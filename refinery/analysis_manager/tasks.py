'''
Created on Apr 5, 2012

@author: nils
'''

from core.models import Analysis, AnalysisResult, WorkflowFilesDL
from analysis_manager.models import AnalysisStatus
from refinery_repository.models import Assay, RawData
from celery.task import task
from celery.task.sets import subtask, TaskSet
import time, os, copy, urllib2
from django.conf import settings
from galaxy_connector.connection import Connection
from workflow_manager.tasks import configure_workflow
from datetime import datetime
from celery.task import chord
from celery.utils import uuid
from celery.task.chords import Chord
from celery import current_app as celery
from file_store.models import FileStoreItem, is_local
from file_store.tasks import import_file, create

# example from: http://www.manasupo.com/2012/03/chord-progress-in-celery.html
class progress_chord(object):
    Chord = Chord

    def __init__(self, tasks, **options):
        self.tasks = tasks
        self.options = options

    def __call__(self, body, **options):
        tid = body.options.setdefault("task_id", uuid())
        r = self.Chord.apply_async((list(self.tasks), body), self.options, **options)
        return body.type.app.AsyncResult(tid), r

@task
def chord_execution(ret_val, analysis):
    
    analysis = Analysis.objects.filter(uuid=analysis.uuid)[0]
    analysis_status = AnalysisStatus.objects.filter(analysis=analysis)[0]
    
    execution_taskset = []; 
    execution_taskset.append(monitor_analysis_execution.subtask((analysis,)) )
    execution_taskset.append(run_analysis_execution.subtask((analysis,)) )
    result_chord, result_set = progress_chord(execution_taskset)(chord_postprocessing.subtask((analysis,)))
     
    # EXECUTION
    ## TESTING NEW DEBUGGING ###
    # execution_monitor_task_id = monitor_analysis_execution.subtask((analysis,)).apply_async().task_id
    #execution_taskset = TaskSet(task=[run_analysis_execution.subtask((analysis,)) ])            
    #result_chord, result_set = progress_chord(execution_taskset)(chord_postprocessing.subtask((analysis,)))
    
    analysis_status.execution_taskset_id = result_set.task_id 
    analysis_status.save()
    
    return

@task
def emptyTask(ret_val):
    return 

@task
def chord_postprocessing (ret_val, analysis):
    
    print "analysis_manager.chord_postprocessing called"
    
    analysis = Analysis.objects.filter(uuid=analysis.uuid)[0]
    analysis_status = AnalysisStatus.objects.filter(analysis=analysis)[0]
    
    # getting list of tasks for download history files
    postprocessing_taskset = download_history_files(analysis)
    
    if len(postprocessing_taskset) < 1:
        #print "---------- less than 1 -----------"
        #temp_task = emptyTask.subtask(("ret_val",))
        temp_task = emptyTask.subtask(("ret_val",))
        result_chord, result_set = progress_chord([temp_task])(chord_cleanup.subtask(analysis=analysis,))
        
    else:
        #print "---------- greater than 1 -----------"
        result_chord, result_set = progress_chord(postprocessing_taskset)(chord_cleanup.subtask(analysis=analysis,))
    
    analysis_status.postprocessing_taskset_id = result_set.task_id 
    analysis_status.save()
    
    print "after chord_postprocessing"   
    return 

@task
def chord_cleanup(ret_val, analysis):
    """
    Code to cleanup galaxy after downloading of results from history
    """
    print "analysis_manager.chord_cleanup called"
    
    analysis = Analysis.objects.filter(uuid=analysis.uuid)[0]
    analysis_status = AnalysisStatus.objects.filter(analysis=analysis)[0]
    
    cleanup_taskset = TaskSet(task=[run_analysis_cleanup.subtask((analysis,)) ])          
    result_chord, result_set = progress_chord(cleanup_taskset)(emptyTask.subtask())
    
    ### TODO ###  UPDATE CLEANUP TASKID FOR ANALYSIS_STATUS
    analysis_status.cleanup_taskset_id = result_set.task_id 
    analysis_status.save()
    
    print "after chord_cleanup"   
    return

# task: run analysis (outermost task, calls subtasks that monitor and run preprocessing, execution, postprocessing)
@task()
def run_analysis(analysis, interval=5.0):
    
    print "analysis_manager.tasks run_analysis called"
    
    analysis_status = AnalysisStatus.objects.get(analysis=analysis)
    
    # DOWNLOADING
    # GETTING LIST OF DOWNLOADED REMOTE FILES 
    datainputs = analysis.workflow_data_input_maps.all()
    download_tasks = []
  
    for files in datainputs:
        #for cur_file in curr_raw:
        # calling filestore on remote file
        #print "calling filestore"
        cur_fs_uuid = files.data_uuid
        #print cur_fs_uuid
        if not is_local(cur_fs_uuid):
            #print "not_local"
            task_id = import_file.subtask((cur_fs_uuid, False,))
            download_tasks.append(task_id)

    
    # PREPROCESSING            
    task_id = run_analysis_preprocessing.subtask( (analysis,) ) 
    download_tasks.append(task_id)
    result_chord, result_set = progress_chord(download_tasks)(chord_execution.subtask(analysis=analysis,))
    # DEBUG
    #result_chord, result_set = progress_chord(download_tasks)(emptyTask.subtask())
    
    # saving preprocessing taskset
    analysis_status.preprocessing_taskset_id = result_set.task_id 
    analysis_status.save()
    
    return

# task: perform postprocessing (innermost task, does the actual work)
@task()
def run_analysis_preprocessing(analysis):
    
    print "analysis_manager.run_analysis_preprocessing called"
    
    # obtain expanded workflow
    connection = get_analysis_connection(analysis)
    
    # creates new library in galaxy
    library_id = connection.create_library("Refinery Analysis - " + str(analysis.uuid) + " (" + str(datetime.now()) + ")");
    
    ### generates same ret_list purely based on analysis object ###
    ret_list = get_analysis_config(analysis)

    # getting expanded workflow configured based on input: ret_list
    new_workflow, history_download = configure_workflow(analysis.workflow.uuid, ret_list, connection)
    
    #print "history_download"
    #print history_download
    
    # saving ouputs of workflow to download 
    for file_dl in history_download:
        temp_dl = WorkflowFilesDL(step_id=file_dl['step_id'], pair_id=file_dl['pair_id'], filename=file_dl['name'])
        temp_dl.save()
        analysis.workflow_dl_files.add( temp_dl ) 
        analysis.save()
            
    # import newly generated workflow 
    new_workflow_info = connection.import_workflow(new_workflow);
    
    ######### ANALYSIS MODEL 
    new_workflow_steps = len(new_workflow["steps"])
    
    # creates new history in galaxy
    history_id = connection.create_history("Refinery Analysis - " + str(analysis.uuid) + " (" + str(datetime.now()) + ")")
    
    # updating analysis object
    analysis.workflow_copy = new_workflow
    analysis.workflow_steps_num = new_workflow_steps
    analysis.workflow_galaxy_id = new_workflow_info['id']
    analysis.library_id = library_id
    analysis.history_id = history_id
    analysis.save()
    
    return

# task: monitor workflow execution (calls subtask that does the actual work)
@task()
def monitor_analysis_execution(analysis, interval=5.0, task_id=None):    

    # required to get updated state (move out of this function) 
    analysis = Analysis.objects.filter(uuid=analysis.uuid)[0]
    analysis_status = AnalysisStatus.objects.filter(analysis=analysis)[0]
    
    # start monitoring task
    if analysis_status.execution_monitor_task_id is None:
        #print "TASKTASKTASKTASK :::: "
        #print monitor_analysis_execution.request.id
        analysis_status.execution_monitor_task_id = monitor_analysis_execution.request.id
        analysis_status.save()
    
    connection = get_analysis_connection(analysis)
    revoke_task = False
    
    while not revoke_task:
        #print  "Sleeping ..."
        progress = connection.get_progress(analysis.history_id)
        monitor_analysis_execution.update_state(state="PROGRESS", meta=progress)
        #print progress
        
        #print  "Awake ..."
        #print  "Analysis Execution Task State: " + analysis_execution_task.state + "\n"
        #print  "Workflow State: " + progress["workflow_state"] + "\n"
        
        if progress["workflow_state"] == "error":
            revoke_task = True
        elif progress["workflow_state"] == "ok":
            revoke_task = True
        #elif progress["workflow_state"] == "queued":
        #    print "Workflow running."
        #elif progress["workflow_state"] == "new":
        #    print "Workflow being prepared."
            
        if not revoke_task:
            time.sleep( interval );
        
    print "revoking/KILLING task finished monitoring task"

# task: perform execution (innermost task, does the actual work)
@task()
def run_analysis_execution(analysis):
    
    print "analysis_manager.run_analysis_execution called"
    
    analysis = Analysis.objects.filter(uuid=analysis.uuid)[0]
    
    ######################
    ### EXECUTION ###
    ######################
    connection = get_analysis_connection(analysis)
    
    ### generates same ret_list purely based on analysis object ###
    ret_list = get_analysis_config(analysis)

    #### NEED TO IMPORT TO GALAXY TO GET GALAXY_IDS ###
    ret_list = import_analysis_in_galaxy(ret_list, analysis.library_id, connection)
          
    # Running workflow 
    result = connection.run_workflow2(analysis.workflow_galaxy_id, ret_list, analysis.history_id)  
    
    return

# task: perform postprocessing (innermost task, does the actual work)
@task()
def run_analysis_postprocessing(analysis):
    
    print "analysis_manager.run_analysis_postprocessing called"
    
    ######################
    ### POSTPROCESSING ###
    ######################      
    # 1. dowloads results from history
    # 2. delete dynamic workflow in galaxy
    # 3. delete history 
    # 4. delete specified library
    
    analysis = Analysis.objects.filter(uuid=analysis.uuid)[0]
    analysis_status = AnalysisStatus.objects.filter(analysis=analysis)[0]
    
    ### ----------------------------------------------------------------#
    # Downloading results from history
    task_list = download_history_files(analysis)
    
    print "downloading history task_list"
    #print task_list
    
    return

# task: perform cleanup, after download of results cleanup galaxy run
@task()
def run_analysis_cleanup(analysis):
    print "analysis_manager.run_analysis_cleanup called"
    
    analysis = Analysis.objects.filter(uuid=analysis.uuid)[0]
    
    # gets current galaxy connection
    connection = get_analysis_connection(analysis)
    
    # delete workflow 
    del_workflow_id = connection.delete_workflow(analysis.workflow_galaxy_id);
    
    # delete history
    connection.delete_history(analysis.history_id)
    
    # delete_library
    connection.delete_library(analysis.library_id)
    
    return

@task()
def get_analysis_config(analysis):
    ###############################################################
    ### TEST RECREATING RET_LIST DICTIONARY FROM ANALYSIS MODEL ###
    curr_workflow = analysis.workflow
    
    # getting distinct workflow inputs
    workflow_data_inputs = curr_workflow.data_inputs.all()
    annot_inputs = {};
    for data_input in workflow_data_inputs:
        input_type = data_input.name
        annot_inputs[input_type] = None;
    
    ret_list = [];
    ret_item = copy.deepcopy(annot_inputs)
    
    temp_count = 0
    temp_len = len(annot_inputs)
    t2 = analysis.workflow_data_input_maps.all().order_by('pair_id')
    for wd in t2:
        if ret_item[wd.workflow_data_input_name] is None:
            ret_item[wd.workflow_data_input_name] = {}
            ret_item[wd.workflow_data_input_name]['pair_id'] = wd.pair_id
            ret_item[wd.workflow_data_input_name]['assay_uuid'] = wd.data_uuid
            ret_item[wd.workflow_data_input_name]['filename'] = wd.fileurl
            temp_count += 1
       
        if temp_count == temp_len:
            ret_list.append(ret_item)
            ret_item = copy.deepcopy(annot_inputs)
            temp_count = 0
            
    #print "ret_list"
    #print ret_list
    
    return ret_list

@task()
def import_analysis_in_galaxy(ret_list, library_id, connection):
    """
    Take workflow configuration and import files into galaxy
    assign galaxy_ids to ret_list
    """
    print "analysis_manager.tasks import_analysis_in_galaxy called"
    
    for fileset in ret_list:
        for k, v in fileset.iteritems():
            cur_item = fileset[k]
            
            # getting current filestoreitem
            curr_filestore = FileStoreItem.objects.get(uuid=cur_item['assay_uuid'])
            #print "got curr_filestore item"
            #print curr_filestore.datafile.path
            #print curr_filestore.datafile.url
            
            file_path = curr_filestore.datafile.path
            cur_item["filepath"] = file_path
            file_id = connection.put_into_library(library_id, file_path)
            cur_item["id"] = file_id
    
    return ret_list

@task
def download_history_files(analysis) :
    """
    Download entire histories from galaxy. Getting files out of history to file store
    """
    
    print "analysis_manger.download_history_files called"
    
    # retrieving list of files to download for workflow
    analysis = Analysis.objects.filter(uuid=analysis.uuid)[0]
    dl_files = analysis.workflow_dl_files
    
    ### creating dicionary based on files to download predetermined by workflow w/ keep operators
    dl_dict = {}
    
    for dl in dl_files.all():
        temp_dict = {}
        temp_dict['filename'] = dl.filename
        temp_dict['pair_id'] = dl.pair_id
        dl_dict[str(dl.step_id)] = temp_dict
    
    # gets current galaxy connection
    connection = get_analysis_connection(analysis)
    
    download_list = connection.get_history_file_list(analysis.history_id)
    task_list = []
    
    # Iterating through files in current galaxy history
    for results in download_list:
        
        # download file if result state is "ok"
        if results['state'] == 'ok':
            file_type = results["type"]
            
            curr_file_id = results['name'] 
            
            if curr_file_id in dl_dict:
                curr_dl_dict = dl_dict[curr_file_id]
                
                #print "#######results"
                #print "found in dict"
                #print results
                
                result_name = curr_dl_dict['filename'] + '.' + file_type
            
            # checks to see if history file is raw fastq file, excluding from download
            #check_fastq = file_type.lower().find('fastq')
            #check_sam = file_type.lower().find('sam')
            #print "checking file types:"
            #print "check_fastq"
            #print check_fastq
            #print "check_sam"
            #print check_sam
            
            
            #if (check_fastq < 0 and check_sam < 0):
                # name of file
                #result_name = results['name'] + '.' + file_type
                # size of file defined by galaxy
                file_size = results['file_size']
                # URL to download
                download_url = connection.make_url(str(results['dataset_id']), is_data=True)
                
                # getting file_store_uuid
                filestore_uuid = create(download_url)
                
                # adding history files to django model 
                temp_file = AnalysisResult(analysis_uuid=analysis.uuid, file_store_uuid=filestore_uuid, file_name=result_name, file_type=file_type)
                temp_file.save() 
                analysis.results.add(temp_file) 
                analysis.save() 
                
                # downloading analysis results into file_store
                # only download files if size is greater than 1
                if file_size > 0:
                    task_id = import_file.subtask((filestore_uuid, False, False, file_size,))
                    task_list.append(task_id)
            
    return task_list
        
@task()
def get_analysis_connection(analysis): 
    """
    gets current connection based on workflow engine associated with imported workflows
    """
    
    cur_workflow = analysis.workflow
    
    connection = Connection(cur_workflow.workflow_engine.instance.base_url,
                             cur_workflow.workflow_engine.instance.data_url,
                             cur_workflow.workflow_engine.instance.api_url,
                             cur_workflow.workflow_engine.instance.api_key)
    return connection

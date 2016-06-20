from rest_framework import serializers

from .models import Workflow, NodeGroup


class NodeGroupSerializer(serializers.ModelSerializer):
    nodes_ids = serializers.PrimaryKeyRelatedField(many=True,
                                                   read_only=True,
                                                   required=False)

    class Meta:
        model = NodeGroup
        fields = ('id', 'uuid', 'node_count', 'is_implicit', 'study',
                  'assay', 'is_current', 'nodes_ids', 'name')

    def create(self, validated_data):
        node_group = NodeGroup.objects.create(
            study=validated_data.get('study'),
            assay=validated_data.get('assay'),
            name=validated_data.get('name'),
            is_current=validated_data.get('is_current')
        )
        """Had to add nodes_ids after group creation. List does not show up in
        validate_data due to read_only attribute."""
        if self.initial_data.get('nodes_ids'):
            node_group.nodes_ids.add(*self.initial_data.get('nodes_ids'))
            node_group.node_count = len(self.initial_data.get('nodes_ids'))
            node_group.save()

        return node_group

    def update(self, instance, validated_data):
        """
        Update and return an existing `NodeGroup` instance, given the
        validated data.
        """
        if self.initial_data.get('nodes_ids'):
            instance.nodes_ids = self.initial_data.get('nodes_ids',
                                                       instance.nodes_ids)
            instance.node_count = len(self.initial_data.get('nodes_ids'))

        instance.is_current = validated_data.get('is_current',
                                                 instance.is_current)
        instance.save()
        return instance


class WorkflowSerializer(serializers.HyperlinkedModelSerializer):
    instance = serializers.HyperlinkedIdentityField(
        view_name='workflow-detail')
    workflow_engine = serializers.StringRelatedField()
    data_inputs = serializers.StringRelatedField()
    input_relationships = serializers.StringRelatedField()

    class Meta:
        model = Workflow

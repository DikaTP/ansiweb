from rest_framework import serializers
from rest_framework.reverse import reverse
from main import models

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.User
		fields = (
			'id',
			'username',
			'email',
			'name',
			'password',
			)
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):

		user = models.User(
			username = validated_data['username'],
			email = validated_data['email'],
			name = validated_data['name']
			)

		user.set_password(validated_data['password'])
		user.save()

		return user

class UserListSerializer(serializers.ModelSerializer):

	url_path = serializers.SerializerMethodField()

	class Meta:
		model = models.User
		fields = (
			'id',
			'username',
			'email',
			'name',
			'password',
			'url_path',
			)
		extra_kwargs = {'password': {'write_only': True}}


	def get_url_path(self, obj):

		request = self.context.get('request')
		obj_url = obj.get_absolute_url()
		return request.build_absolute_uri(obj_url)


class MachineCredentialSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = models.MachineCredential
		fields = (
			'ssh_username',
			'ssh_pass',
			'privilege_pass',
			)

class AwsCredentialSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.AwsCredential
		fields = (
			'access_key',
			'secret_access_key',
			)

class CredentialSerializer(serializers.ModelSerializer):

	machine_detail = MachineCredentialSerializer(required=False, many=False)
	aws_detail = AwsCredentialSerializer(required=False, many=False)

	class Meta:
		model = models.Credential
		fields = (
			'id',
			'user',
			'name',
			'description',
			'credential_type',
			'machine_detail',
			'aws_detail',
			)
		extra_kwargs = {'user': {'read_only': True}}

	def create(self, validated_data):

		machine_cred_data = validated_data.pop('machine_detail')
		aws_cred_data = validated_data.pop('aws_detail')
		credential = models.Credential.objects.create(**validated_data)
		if credential.credential_type == 'machine':
			models.MachineCredential.objects.create(credential=credential, **machine_cred_data)
		else:
			models.AwsCredential.objects.create(credential=credential, **aws_cred_data)
		return credential

	def update(self, instance, validated_data):

		if instance.credential_type == 'machine':
			machine_cred_data = validated_data.pop('machine_detail')
			machinecred = instance.machine_detail
		else:
			aws_cred_data = validated_data.pop('aws_detail')
			awscred = instance.aws_detail

			instance.name = validated_data.get('name', instance.name)
			instance.description = validated_data.get('description', instance.description)

		if instance.credential_type == 'machine':
			machinecred.ssh_username = machine_cred_data.get('ssh_username', machinecred.ssh_username)
			machinecred.ssh_pass = machine_cred_data.get('ssh_pass', machinecred.ssh_pass)
			machinecred.privilege_pass = machine_cred_data.get('privilege_pass', machinecred.privilege_pass)
			machinecred.save()
		elif instance.credential_type == 'aws':
			awscred.access_key = aws_cred_data.get('access_key', awscred.access_key)
			awscred.secret_access_key = aws_cred_data.get('secret_access_key', awscred.secret_access_key)
			awscred.save()
		return instance

	def validate(self, data):

		data = super(CredentialSerializer, self).validate(data)
		if not any([data.get('machine_detail'), data.get('aws_detail')]):
			raise serializers.ValidationError('error')
		return data

	def get_extra_kwargs(self):

		extra_kwargs = super(CredentialSerializer, self).get_extra_kwargs()
		action = self.context['view'].action

		if action in ['update', 'partial_update']:
			cred_type_kwargs = extra_kwargs.get('credential_type', {})
			cred_type_kwargs['read_only'] = True
			extra_kwargs['credential_type'] = cred_type_kwargs

		return extra_kwargs

class CredentialReadSerializer(serializers.ModelSerializer):

	credential_type_detail = serializers.SerializerMethodField()

	class Meta:
		model = models.Credential
		fields = (
			'id',
			'user',
			'name',
			'description',
			'credential_type',
			'credential_type_detail'
			)
		extra_kwargs = {'user': {'read_only': True}}

	def get_credential_type_detail(self, obj):
		
		if obj.credential_type == 'machine':
			detail = models.MachineCredential.objects.get(id = obj.machine_detail.id)
			return MachineCredentialSerializer(detail).data
		else:
			detail = models.AwsCredential.objects.get(id = obj.aws_detail.id)
			return AwsCredentialSerializer(detail).data

class CredentialListSerializer(CredentialReadSerializer):

	url_path = serializers.SerializerMethodField()

	class Meta(CredentialReadSerializer.Meta):
		fields = CredentialReadSerializer.Meta.fields + ('url_path',)

	def get_url_path(self, obj):

		request = self.context.get('request')
		obj_url = obj.get_absolute_url()
		return request.build_absolute_uri(obj_url)

class CredChoiceField(serializers.PrimaryKeyRelatedField):

	def get_queryset(self):

		user = self.context['request'].user
		if user.is_staff == False:
			queryset = models.Credential.objects.filter(user=user)
		else:
			queryset = models.Credential.objects.all()
		return queryset

class InventorySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Inventory
		fields = (
			'id',
			'user',
			'description',
			'file',
			)
		extra_kwargs = {'user': {'read_only': True}}

class InventoryListSerializer(InventorySerializer):

	url_path = serializers.SerializerMethodField()

	class Meta(InventorySerializer.Meta):
		fields = InventorySerializer.Meta.fields + ('url_path',)

	def get_url_path(self, obj):

		request = self.context.get('request')
		obj_url = obj.get_absolute_url()
		return request.build_absolute_uri(obj_url)

class InvChoiceField(serializers.PrimaryKeyRelatedField):

	def get_queryset(self):

		user = self.context['request'].user
		if user.is_staff == False:
			queryset = models.Inventory.objects.filter(user=user)
		else:
			queryset = models.Inventory.objects.all()
		return queryset


class PlaybookSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Playbook
		fields = (
			'id',
			'user',
			'description',
			'file',
			)
		extra_kwargs = {'user': {'read_only': True}}

class PlaybookListSerializer(PlaybookSerializer):

	url_path = serializers.SerializerMethodField()

	class Meta(PlaybookSerializer.Meta):
		fields = PlaybookSerializer.Meta.fields + ('url_path',)

	def get_url_path(self, obj):

		request = self.context.get('request')
		obj_url = obj.get_absolute_url()
		return request.build_absolute_uri(obj_url)

class PbChoiceField(serializers.PrimaryKeyRelatedField):

	def get_queryset(self):

		user = self.context['request'].user
		if user.is_staff == False:
			queryset = models.Playbook.objects.filter(user=user)
		else:
			queryset = models.Playbook.objects.all()
		return queryset


class PlaybookJobSerializer(serializers.ModelSerializer):

	playbook = PbChoiceField()

	class Meta:
		model = models.PlaybookJob
		fields = ('playbook',)

class AdhocJobSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.AdhocJob
		fields = ('module', 'arguments',)

class JobSerializer(serializers.ModelSerializer):

	playbook_detail = PlaybookJobSerializer(required=False, many=False)
	adhoc_detail = AdhocJobSerializer(required=False, many=False)
	inventory = InvChoiceField()
	credential = CredChoiceField()

	class Meta:
		model = models.Job
		fields = (
			'id',
			'user',
			'name',
			'job_type',
			'description',
			'inventory',
			'credential',
			'verbosity',
			'privilege_flag',
			'playbook_detail',
			'adhoc_detail',
			)
		extra_kwargs = {'user': {'read_only': True}} 

	def create(self, validated_data):

		playbook_job_data = validated_data.pop('playbook_detail')
		adhoc_job_data = validated_data.pop('adhoc_detail')
		job = models.Job.objects.create(**validated_data)
		if job.job_type == 'pb':
			models.PlaybookJob.objects.create(job=job, **playbook_job_data)
		else:
			models.AdhocJob.objects.create(job=job, **adhoc_job_data)
		return job

	def update(self, instance, validated_data):

		if instance.job_type == 'pb':
			playbook_job_data = validated_data.pop('playbook_detail')
			playbookjob = instance.playbook_detail
		else:
			adhoc_job_data = validated_data.pop('adhoc_detail')
			adhocjob = instance.adhoc_detail

		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.inventory = validated_data.get('inventory', instance.inventory)
		instance.credential = validated_data.get('credential', instance.credential)
		instance.verbosity = validated_data.get('verbosity', instance.verbosity)
		instance.privilege_flag = validated_data.get('privilege_flag', instance.privilege_flag)
		instance.save()

		if instance.job_type == 'pb':
			playbookjob.playbook = playbook_job_data.get('playbook', playbookjob.playbook)
			playbookjob.save()
		elif instance.job_type == 'adhoc':
			adhocjob.module = adhoc_job_data.get('module', adhocjob.module)
			adhocjob.arguments = adhoc_job_data.get('arguments', adhocjob.arguments)
			adhocjob.save()

		return instance

	def validate(self, data):

		data = super(JobSerializer, self).validate(data)
		if not any([data.get('playbook_detail'), data.get('adhoc_detail')]):
			raise serializers.ValidationError('error')
		return data

	def get_extra_kwargs(self):

		extra_kwargs = super(JobSerializer, self).get_extra_kwargs()
		action = self.context['view'].action

		if action in ['update', 'partial_update']:
			job_type_kwargs = extra_kwargs.get('job_type', {})
			job_type_kwargs['read_only'] = True
			extra_kwargs['job_type'] = job_type_kwargs

		return extra_kwargs

class JobReadSerializer(serializers.ModelSerializer):
	job_type_detail = serializers.SerializerMethodField()

	class Meta:
		model = models.Job
		fields = (
			'id',
			'name',
			'job_type',
			'description',
			'inventory',
			'credential',
			'verbosity',
			'privilege_flag',
			'job_type_detail',
			)
		extra_kwargs = {'job_type': {'read_only': True}}

	def get_job_type_detail(self, obj):
		
		if obj.job_type == 'pb':
			detail = models.PlaybookJob.objects.get(id = obj.playbook_detail.id)
			return PlaybookJobSerializer(detail).data
		else:
			detail = models.AdhocJob.objects.get(id = obj.adhoc_detail.id)
			return AdhocJobSerializer(detail).data

class JobListSerializer(JobReadSerializer):

	url_path = serializers.SerializerMethodField()

	class Meta(JobReadSerializer.Meta):
		fields = JobReadSerializer.Meta.fields + ('url_path',)

	def get_url_path(self, obj):

		request = self.context.get('request')
		obj_url = obj.get_absolute_url()
		return request.build_absolute_uri(obj_url)

class BaseHistorySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.History
		fields = (
			'date',
			'status',
			'job',
			)

class HistorySerializer(BaseHistorySerializer):

	url_path = serializers.SerializerMethodField()

	class Meta(BaseHistorySerializer.Meta):
		fields = BaseHistorySerializer.Meta.fields + ('url_path',)

	def get_url_path(self, obj):

		request = self.context.get('request')
		obj_url = obj.get_absolute_url()
		return request.build_absolute_uri(obj_url)


class HistoryDetailSerializer(BaseHistorySerializer):

	class Meta(BaseHistorySerializer.Meta):
		fields = BaseHistorySerializer.Meta.fields + ('result', 'runtime')
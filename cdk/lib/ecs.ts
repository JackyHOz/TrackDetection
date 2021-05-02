import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import * as ecs from '@aws-cdk/aws-ecs';
import { join } from 'path';
import * as iam from '@aws-cdk/aws-iam';

interface WebStackprops extends cdk.StackProps {
	mainvpc: ec2.IVpc;
	ecssg: ec2.SecurityGroup;
	lb: elbv2.ApplicationLoadBalancer;
}

export class EcsStack extends cdk.Stack {
	public readonly service: ecs.FargateService;
	constructor(scope: cdk.App, id: string, props: WebStackprops) {
		super(scope, id, props);
		const lb = props.lb;
		const ecssg = props.ecssg;
		const vpc = props.mainvpc;

		const cluster = new ecs.Cluster(this, 'ECSCluster', {
			vpc: vpc,
		});

		const dockerrole = new iam.Role(this, 'ECSRole', {
			assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
			roleName: 'ECSRole',
		});
		// create role for ecs
		dockerrole.addManagedPolicy(
			iam.ManagedPolicy.fromAwsManagedPolicyName('AdministratorAccess'),
		);

		// config task
		const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef', {
			cpu: 2048,
			memoryLimitMiB: 4096,
			taskRole: dockerrole,
			executionRole: dockerrole,
		});

		// ecs images create from local dockerfile
		const container = taskDefinition.addContainer('ecs', {
			image: ecs.ContainerImage.fromAsset(join(__dirname, '..', '..', 'web'), {
				file: 'Dockerfile',
			}),
			// save ecs log
			logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'ecs-log' }),
		});

		// run service in private subnet
		this.service = new ecs.FargateService(this, 'FargateService', {
			cluster,
			taskDefinition,
			securityGroups: [ecssg],
			vpcSubnets: vpc.selectSubnets({ subnetGroupName: 'ECS' }),
		});

		// create auto scaling in fargate
		const scaling = this.service.autoScaleTaskCount({
			minCapacity: 1,
			maxCapacity: 5,
		});

    scaling.scaleOnCpuUtilization('CPU_Utilization', {
      targetUtilizationPercent: 80,
    });

		container.addPortMappings({
			containerPort: 5000,
			hostPort: 5000,
			protocol: ecs.Protocol.TCP,
		});

		const listener = lb.addListener('Listener', { port: 80 });
		// add target group to alb
		const targetGroup = listener.addTargets('ECS', {
			port: 5000,
			protocol: elbv2.ApplicationProtocol.HTTP,
			targets: [this.service],
		});
	}
}

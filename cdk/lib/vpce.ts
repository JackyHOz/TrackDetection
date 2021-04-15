import * as ec2 from '@aws-cdk/aws-ec2';
import * as cdk from '@aws-cdk/core';

interface Stackprops extends cdk.StackProps {
  mainvpc: ec2.IVpc;
  vpcesg: ec2.SecurityGroup;
}

export class VpceStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: Stackprops) {
    super(scope, id, props);
    const vpc = props.mainvpc;
    const vpcesg = props.vpcesg;

    // create 3 vpc endpoint : kvs, ecr, rekognition
    const vpce = new ec2.InterfaceVpcEndpoint(this, 'KinesisStreamsInterfaceEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.KINESIS_STREAMS,
      vpc,
      privateDnsEnabled: true,
      subnets: vpc.selectSubnets({
        subnetGroupName: 'ECS',
      }),
      securityGroups: [vpcesg],
    });

    const vpce1 = new ec2.InterfaceVpcEndpoint(this, 'ECRInterfaceEndpoint', {
        service: ec2.InterfaceVpcEndpointAwsService.ECR,
        vpc,
        privateDnsEnabled: true,
        subnets: vpc.selectSubnets({
          subnetGroupName: 'ECS',
        }),
        securityGroups: [vpcesg],
      });

    vpc.addGatewayEndpoint('s3-gateway', {
      service: ec2.GatewayVpcEndpointAwsService.S3,
      subnets: [{
            subnetName: 'ECS'
      }]
    });

    const vpce2 = new ec2.InterfaceVpcEndpoint(this, 'RekognitionInterfaceEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.REKOGNITION,
      vpc,
      privateDnsEnabled: true,
      subnets: vpc.selectSubnets({
        subnetGroupName: 'ECS',
      }),
      securityGroups: [vpcesg],
    });

  }
} 
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';

export class CdkStack extends cdk.Stack {
  public readonly vpc: ec2.IVpc
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // create vpc
    this.vpc = new ec2.Vpc(this, 'VPC', {
      cidr: "10.10.0.0/16",
      maxAzs: 2,
      subnetConfiguration: [ 
        { name: 'PUBLIC', subnetType: ec2.SubnetType.PUBLIC},
        { name: 'ECS', subnetType: ec2.SubnetType.PRIVATE },
      ],
      //add NAT Gateway in VPC 
      natGateways: 1,
  
    });

  }
}

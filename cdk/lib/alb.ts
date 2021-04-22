import * as ec2 from '@aws-cdk/aws-ec2';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import * as cdk from '@aws-cdk/core';

interface AlbStackprops extends cdk.StackProps {
  mainvpc: ec2.IVpc,
  albsg: ec2.SecurityGroup;
}

export class AlbStack extends cdk.Stack {
  public readonly lb:elbv2.ApplicationLoadBalancer
  constructor(scope: cdk.App, id: string, props: AlbStackprops) {
    super(scope, id, props);
    // get props of vpc and ALB security group
    const vpc = props.mainvpc;
    const albsg = props.albsg;
    // create ALB
    this.lb = new elbv2.ApplicationLoadBalancer(this, 'LB', {
      // place in VPC
      vpc,
      // enable internet facing
      internetFacing: true, 
      // attach albsg props
      securityGroup: albsg,
      // plcae in public AZs
      vpcSubnets: vpc.selectSubnets({subnetType: ec2.SubnetType.PUBLIC})
    });

  }
}
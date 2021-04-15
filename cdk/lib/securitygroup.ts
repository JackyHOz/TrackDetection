import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';

interface SecurityGroupStackprops extends cdk.StackProps {
  mainvpc: ec2.IVpc;
}

export class SecurityGroupStack extends cdk.Stack {
  public readonly ecssg:ec2.SecurityGroup;
  public readonly vpcesg:ec2.SecurityGroup;
  constructor(scope: cdk.App, id: string, props: SecurityGroupStackprops) {
    super(scope, id, props);
    // get props of vpc
    const vpc = props.mainvpc;
    // create security group for ecs
    this.ecssg = new ec2.SecurityGroup(this, "ECSSG", {
        vpc,
        securityGroupName: 'ECSSecurityGroup',
        allowAllOutbound: true ,
      });

    this.ecssg.addIngressRule(
        this.ecssg,
        // may be change port later
        ec2.Port.tcp(443),
        "allow public https access from ECSSG"
      );
    
    // create security group for endpoint
    this.vpcesg = new ec2.SecurityGroup(this, "VPCESG", {
      vpc,
      securityGroupName: 'VPCESecurityGroup',
      allowAllOutbound: false,
    });
    
    this.vpcesg.addIngressRule(
      this.ecssg,
      ec2.Port.tcp(443),
      "allow HTTPS access "
    );
  }
}
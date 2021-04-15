import * as iam from '@aws-cdk/aws-iam';
import * as cdk from '@aws-cdk/core';

export class RoleStack extends cdk.Stack  {
  public readonly dockerrole: iam.Role;
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // create role for docker
    this.dockerrole = new iam.Role(this, 'ECSRole', {
      assumedBy: new iam.CompositePrincipal(
        new iam.ServicePrincipal('ecs.amazonaws.com'),
        new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      ),
      roleName: 'ECSRole'
    });

    this.dockerrole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AdministratorAccess'))
    // dockerrole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName(''))

  }
}
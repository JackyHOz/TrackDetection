#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { CdkStack } from '../lib/cdk-stack';
// import { EcrStack } from '../lib/ecr';
import { SecurityGroupStack } from '../lib/securitygroup';
import { VpceStack } from '../lib/vpce';
import { EcsStack} from '../lib/ecs';
import { AlbStack } from '../lib/alb';

const app = new cdk.App();
const env = {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
}       
const vpc = new CdkStack(app, 'CdkStack', {env: env});
const sg = new SecurityGroupStack(app, 'SGStack', {env: env, mainvpc: vpc.vpc});
const vpce = new VpceStack(app, 'VpceStack', {env: env, mainvpc: vpc.vpc, vpcesg: sg.vpcesg});
const alb = new AlbStack(app, 'AlbStack', {env: env, mainvpc: vpc.vpc, albsg: sg.albsg})
const ecs = new EcsStack(app, 'EcsStack', {env: env, mainvpc: vpc.vpc, ecssg: sg.ecssg, lb: alb.lb});
// const ecr = new EcrStack(app, 'EcrStack', {env: env, mainvpc: vpc.vpc, vpcesg: sg.vpcesg});
 
targetScope = 'subscription'

param location string = 'eastus'
param resourceGroupName string = 'mlops-rg'
param workspaceName string = 'mlops-aml-workspace'
param clusterName string = 'gpu-cluster'
param storageAccountName string = 'mlopsstorageacct0025'
param spnObjectId string
param containerRegistryId string
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
}
module mls './modules/machineLearningService/mls.bicep' = {
  name: 'mls'
  scope: resourceGroup
  params: {
    location: location
    applicationInsightId: appInsights.outputs.applicationInsightId
    workspaceName: workspaceName
    storageAccountId: storageAccount.outputs.storageAccountId
    keyVaultId: vault.outputs.keyVaultId
    containerRegistryId: containerRegistryId
  }
}

module vault './modules/keyvault/kv.bicep' = {
  name: 'vault'
  scope: resourceGroup
  params: {
    keyVaultName: 'mlopskv00286'
    location: location
    tenantId: subscription().tenantId
  }
}
module appInsights './modules/applicationInsights/appInsights.bicep' = {
  name: 'appInsights'
  scope: resourceGroup
  params: {
    applicationInsightsName: 'mlops-app-insights'
    appInsightsLocation: location
  }
}

module mlCompute './modules/machineLearningService/ml_compute.bicep' = {
  name: 'mlCompute'
  scope: resourceGroup
  params: {
    location: location
    objectId: spnObjectId
    workspaceName: mls.outputs.workspaceName
    computeName: clusterName
  }
}

module storageAccount './modules/storageAccounts/sa.bicep' = {
  name: 'storageAccount'
  scope: resourceGroup
  params: {
    storageAccountName: storageAccountName
    location: location
  }
}

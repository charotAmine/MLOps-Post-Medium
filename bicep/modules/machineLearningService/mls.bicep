targetScope = 'resourceGroup'
param location string
param workspaceName string
param storageAccountId string
param keyVaultId string
param applicationInsightId string
param containerRegistryId string
resource amlWorkspace 'Microsoft.MachineLearningServices/workspaces@2022-10-01' = {
  name: workspaceName
  location: location
  identity: {
    type: 'systemAssigned'
  }
  properties: {
    friendlyName: workspaceName
    storageAccount: storageAccountId
    keyVault: keyVaultId
    applicationInsights: applicationInsightId
    containerRegistry: containerRegistryId

  }
}

output workspaceName string = amlWorkspace.name

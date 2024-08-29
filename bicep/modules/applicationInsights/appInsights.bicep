param applicationInsightsName string
param appInsightsLocation string

resource insight 'Microsoft.Insights/components@2020-02-02' = {
  name: applicationInsightsName
  location: appInsightsLocation
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

output applicationInsightId string = insight.id

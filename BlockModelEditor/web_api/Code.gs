var server_url = "http://84df39f4.ngrok.io";

function onOpen() {
  SpreadsheetApp.getUi()
      .createMenu('Block Model')
      .addItem('Load Into System', 'openSendConfigurationDialog')
      .addItem('Get Block Model Statistics', 'showStatisticsDialog')
      .addItem('Get Reblocked Model', 'openReblockModelDialog')
      .addToUi();
}

function openSendConfigurationDialog() {
  var html = HtmlService.createHtmlOutputFromFile('BlockModelLoadForm');
  SpreadsheetApp.getUi().showModalDialog(html, 'Load Block Model');
}

function openReblockModelDialog() {
  var html = HtmlService.createHtmlOutputFromFile('ReblockModelForm');
  SpreadsheetApp.getUi().showModalDialog(html, 'Reblock Model');
}

function handleSendForm(formValues) {
  var xColumn = formValues.xPositionColumn + ':' + formValues.xPositionColumn;
  var yColumn = formValues.yPositionColumn + ':' + formValues.yPositionColumn;
  var zColumn = formValues.zPositionColumn + ':' + formValues.zPositionColumn;
  var weightColumn = formValues.weightColumn + ':' + formValues.weightColumn;
  var gradeColumns = formValues.gradeColumns.split(',');
  for (var i = 0; i < gradeColumns.length; i++) {
    gradeColumns[i] = gradeColumns[i] + ':' + gradeColumns[i];
  }
  var columns = [xColumn, yColumn, zColumn, weightColumn, gradeColumns];
  sendBlockModel(columns);
}

function handleReblockForm(formValues) {
  getReblockedModel(formValues.rx, formValues.ry, formValues.rz);
}

function showStatisticsDialog() {
  var statistics = getBlockModelStatistics();
  var statisticsText = "Total Number of Blocks: " + statistics.total_blocks;
  statisticsText += "\nTotal Weight: " + statistics.total_weight;
  statisticsText += "\nTotal Grade: " + statistics.total_grade;
  statisticsText += "\nPercentage of Air: " + statistics.air_percentage + "%";
  
  var ui = SpreadsheetApp.getUi();
  var result = ui.alert('Block Model Statistics', statisticsText, ui.ButtonSet.OK);

}

function getMineralDeposits() {
  var deposits = UrlFetchApp.fetch(server_url + "/mineral_deposits");
  return JSON.parse(deposits.getContentText());
}

function addMineralDeposit(depositName) {
  var url = server_url + "/mineral_deposits"
  var payload = JSON.stringify({"mineral_deposit": {"name": depositName}});
  var options = { "method":"POST", "contentType" : "application/json","payload" : payload };
  var response = UrlFetchApp.fetch(url, options);
}

function getBlockModels() {
  var deposits = UrlFetchApp.fetch(server_url + "/block_models");
  return JSON.parse(deposits.getContentText());
}

function addBlockModel(columns, ores, depositId) {
  var url = server_url + "/block_models"
  var payload = convertColumnsToJson(columns, ores, depositId);
  var options = { "method":"POST", "contentType" : "application/json","payload" : payload };
  var response = UrlFetchApp.fetch(url, options);
}

function getBlockModelStatistics(blockModelId) {
  var statistics = UrlFetchApp.fetch(server_url + "/block_models/" + blockModelId);
  return JSON.parse(statistics.getContentText());
}

function getBlockModelBlocks(blockModelId) {
  var blocks = UrlFetchApp.fetch(server_url + "/block_models/" + blockModelId + "/blocks");
  return JSON.parse(blocks.getContentText());
}

function getBlock(blockModelId, blockId) {
  var block = UrlFetchApp.fetch(server_url + "/block_models/" + blockModelId + "/blocks/" + blockId);
  return JSON.parse(block.getContentText());
}

function getReblockedModel(rx, ry, rz) {
  var url = server_url + "/block_models"
  var payload = JSON.stringify({ 'rx': rx, 'ry': ry, 'rz': rz });
  var options = { "method":"POST", "contentType" : "application/json","payload" : payload };
  var response = UrlFetchApp.fetch(url, options);
  createNewSheetForModel(JSON.parse(response.getContentText()), "Reblocked Model");
}

function createNewSheetForModel(json_block_model, sheetName) {
  var activeSpreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var newSheet = activeSpreadsheet.getSheetByName(sheetName);

  if (newSheet == null) {
    newSheet = activeSpreadsheet.insertSheet();
    newSheet.setName(sheetName);
  }
  
  newSheet.clear();
  for (var i = 0; i < json_block_model.x_positions.length; i++) {
    newSheet.appendRow([json_block_model.x_positions[i], json_block_model.y_positions[i], json_block_model.z_positions[i],
                       json_block_model.weights[i], json_block_model.grades[i]]);
  }
}

function convertColumnsToJson(columns, ores, depositId) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var xPositions = sheet.getRange(columns[0]).getValues().map(function(e){return e[0];});
  var yPositions = sheet.getRange(columns[1]).getValues().map(function(e){return e[0];});
  var zPositions = sheet.getRange(columns[2]).getValues().map(function(e){return e[0];});
  var weights = sheet.getRange(columns[3]).getValues().map(function(e){return e[0];});
  var grades = {};
  for (var i = 0; i < columns[4].length; i++) 
    {
      grades[ores[i]] = sheet.getRange(columns[4][i]).getValues().map(function(e){return e[0];});
    }
  var jsonObject = {'deposit_id': depositId, 'block_model': { 'x_positions': xPositions, 'y_positions': yPositions, 'z_positions': zPositions, 
                                    'weights': weights, 'grades': grades }}
  return JSON.stringify(jsonObject);
}

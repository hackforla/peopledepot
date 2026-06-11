// ═══════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

const CONFIG = {
  EXPECTED_HEADERS: ['table_name', 'column_name', 'data_type', 'is_nullable'],
  EXPECTED_COLUMN_COUNT: 4,
  DIALOG_WIDTH: 400,
  DIALOG_HEIGHT: 250,
  SHEET_NAME_PREFIX: 'table-descriptions',
  LIGHT_GRAY: '#efefef',
  LIGHT_GRAY2: '#d9d9d9',
  DJANGO_SYSTEM_APPS: ['core', 'project'],
  DJANGO_SYSTEM_FIELDS: ['id', 'uuid', 'created_at', 'updated_at'],

  // Column layout: A-F (user input), G-K (CSV data + derived)
  COLUMNS: {
    FIELDS_AUDITED: 1,
    CHANGE_TITLE: 2,
    AUDIT: 3,
    DJANGO_CREATED_TABLE: 4,
    DJANGO_CREATED_FIELD: 5,
    DJANGO_APP_NAME: 6,
    TABLE_NAME: 7,
    TABLE_NAME_PREFIX: 8,
    COLUMN_NAME: 9,
    DATA_TYPE: 10,
    IS_NULLABLE: 11
  },

  COLUMN_WIDTHS: {
    1: 74,    // A: Fields audited
    2: 75,    // B: Change title
    3: 62,    // C: Audit
    4: 74,    // D: Django created Table
    5: 74,    // E: Django created field
    6: 48,    // F: Django app name
    7: 239,   // G: table_name
    8: 206,   // H: table_name-prefix
    9: 157,   // I: column_name
    10: 157,  // J: data_type
    11: 69    // K: is_nullable
  },

  HEADERS: [
    'Fields\naudited\n(✓)',
    'Change\ntitle\nof table',
    'Audit\n(✓/✗)',
    'Django\ncreated\nTable',
    'Django\ncreated\nfield',
    'Django\napp\nname',
    'table_name',
    'table_name-\nprefix',
    'column_name',
    'data_type',
    'is_nullable'
  ]
};

// ═══════════════════════════════════════════════════════════════════════════
// UI & MENU
// ═══════════════════════════════════════════════════════════════════════════

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('CSV Tools')
    .addItem('Upload CSV → New Sheet', 'showUploadDialog')
    .addToUi();
}

function showUploadDialog() {
  const html = HtmlService.createHtmlOutputFromFile('UploadDialog')
    .setWidth(CONFIG.DIALOG_WIDTH)
    .setHeight(CONFIG.DIALOG_HEIGHT);
  SpreadsheetApp.getUi().showModalDialog(html, 'Import CSV File');
}

// ═══════════════════════════════════════════════════════════════════════════
// CSV UPLOAD & VALIDATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Receives Base64-encoded CSV data, decodes, validates, and imports.
 * @param {string} dataUrl - Data URL with base64-encoded CSV
 */
function processUploadedCsv(dataUrl) {
  try {
    if (!dataUrl) {
      alertUser('❌ No file selected. Please try again.');
      return;
    }

    const csvText = decodeBase64Csv(dataUrl);
    const rows = Utilities.parseCsv(csvText);

    validateCsvStructure(rows);
    validateCsvHeaders(rows);
    validateCsvData(rows);

    importCsvWithAllFormulas(rows);
    alertUser('✅ CSV imported successfully!');

  } catch (error) {
    Logger.error(`Import error: ${error.message}`);
    alertUser(`❌ Error importing CSV:\n\n${error.message}`);
  }
}

/**
 * Decode Base64 CSV data from data URL.
 * @param {string} dataUrl - Data URL with base64-encoded CSV
 * @returns {string} Decoded CSV text
 */
function decodeBase64Csv(dataUrl) {
  const base64 = dataUrl.replace(/^data:.*?;base64,/, '');
  return Utilities.newBlob(
    Utilities.base64Decode(base64)
  ).getDataAsString();
}

/**
 * Validate CSV structure (not empty, correct column count).
 * @param {Array<Array<string>>} rows - CSV data
 * @throws {Error} If validation fails
 */
function validateCsvStructure(rows) {
  if (rows.length === 0) {
    throw new Error('CSV file is empty.');
  }

  if (rows[0].length !== CONFIG.EXPECTED_COLUMN_COUNT) {
    throw new Error(
      `CSV must have exactly ${CONFIG.EXPECTED_COLUMN_COUNT} columns.\n\n` +
      `Found: ${rows[0].length}\n\n` +
      'Required columns:\n' +
      '1. table_name\n' +
      '2. column_name\n' +
      '3. data_type\n' +
      '4. is_nullable'
    );
  }
}

/**
 * Validate CSV headers match expected format.
 * @param {Array<Array<string>>} rows - CSV data
 * @throws {Error} If headers don't match
 */
function validateCsvHeaders(rows) {
  const actualHeaders = rows[0].map(h => h.toLowerCase().trim());

  if (!actualHeaders.every((h, i) => h === CONFIG.EXPECTED_HEADERS[i])) {
    throw new Error(
      '❌ CSV headers do not match expected format.\n\n' +
      `Expected: ${CONFIG.EXPECTED_HEADERS.join(', ')}\n` +
      `Got: ${rows[0].join(', ')}`
    );
  }
}

/**
 * Validate CSV data rows for empty cells.
 * @param {Array<Array<string>>} rows - CSV data
 * @throws {Error} If user cancels
 */
function validateCsvData(rows) {
  const dataRows = rows.slice(1);
  const emptyRows = dataRows.filter(row => row.some(cell => cell.trim() === ''));

  if (emptyRows.length === 0) return;

  const response = SpreadsheetApp.getUi().alert(
    `⚠️ Found ${emptyRows.length} row(s) with empty cells.\n\n` +
    'Continue anyway?',
    SpreadsheetApp.getUi().ButtonSet.YES_NO
  );

  if (response !== SpreadsheetApp.getUi().Button.YES) {
    throw new Error('Import cancelled by user.');
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// CSV IMPORT & SHEET CREATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Core import routine – creates sheet with audit columns and formulas.
 * @param {Array<Array<string>>} rows - CSV data including header
 */
function importCsvWithAllFormulas(rows) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheetName = getUniqueSheetName(ss);

  let sheet = ss.getSheetByName(sheetName);
  if (sheet) ss.deleteSheet(sheet);
  sheet = ss.insertSheet(sheetName, 0);

  const dataRowCount = rows.length - 1;

  writeRawCsvData(sheet, rows);
  setupHeaders(sheet);
  applyFormulas(sheet, dataRowCount);
  applyCheckboxValidation(sheet, dataRowCount);
  formatColumns(sheet);
  freezeHeaderRow(sheet);
  hideHelperColumns(sheet);
  applyBackgroundColors(sheet, dataRowCount);
  applyFilter(sheet, dataRowCount);

  Logger.log(`✅ Sheet "${sheetName}" created with ${dataRowCount} rows`);
}

/**
 * Generate unique sheet name based on current date.
 * @param {Spreadsheet} ss - Active spreadsheet
 * @returns {string} Unique sheet name
 */
function getUniqueSheetName(ss) {
  const date = new Date().toISOString().slice(0, 10);
  const baseName = `${CONFIG.SHEET_NAME_PREFIX} ${date}`;
  let name = baseName;
  let counter = 1;

  while (ss.getSheetByName(name)) {
    name = `${baseName} (${counter})`;
    counter++;
  }

  return name;
}

/**
 * Write raw CSV data to columns G–J, then insert column for table_name-prefix.
 * @param {Sheet} sheet - Target sheet
 * @param {Array<Array<string>>} rows - CSV data
 */
function writeRawCsvData(sheet, rows) {
  sheet.getRange(1, CONFIG.COLUMNS.TABLE_NAME, rows.length, CONFIG.EXPECTED_COLUMN_COUNT)
    .setValues(rows);
  sheet.insertColumnAfter(CONFIG.COLUMNS.TABLE_NAME);
}

/**
 * Set up header row with formatting.
 * @param {Sheet} sheet - Target sheet
 */
function setupHeaders(sheet) {
  const headerRange = sheet.getRange(1, 1, 1, CONFIG.HEADERS.length);
  headerRange.setValues([CONFIG.HEADERS]);
  headerRange.setFontWeight('bold');
  headerRange.setWrap(true);
  headerRange.setVerticalAlignment('middle');
}

/**
 * Apply formulas to derived columns (rows 2 onwards).
 * @param {Sheet} sheet - Target sheet
 * @param {number} dataRowCount - Number of data rows
 */
function applyFormulas(sheet, dataRowCount) {
  if (dataRowCount === 0) return;

  const { DJANGO_APP_NAME, TABLE_NAME, TABLE_NAME_PREFIX, DJANGO_CREATED_FIELD, DJANGO_CREATED_TABLE, COLUMN_NAME } = CONFIG.COLUMNS;

  // Column F: Django app name (LEFT of G up to first "_")
  sheet
    .getRange(2, DJANGO_APP_NAME, dataRowCount, 1)
    .setFormulaR1C1(`=IFERROR(LEFT(RC[${TABLE_NAME - DJANGO_APP_NAME}], FIND("_", RC[${TABLE_NAME - DJANGO_APP_NAME}]) - 1), RC[${TABLE_NAME - DJANGO_APP_NAME}])`);

  // Column H: table_name-prefix (RIGHT of G after first "_")
  sheet
    .getRange(2, TABLE_NAME_PREFIX, dataRowCount, 1)
    .setFormulaR1C1(`=IFERROR(RIGHT(RC[${TABLE_NAME - TABLE_NAME_PREFIX}], LEN(RC[${TABLE_NAME - TABLE_NAME_PREFIX}]) - FIND("_", RC[${TABLE_NAME - TABLE_NAME_PREFIX}])), "")`);

  // Column E: Django created field (check against system fields)
  sheet
    .getRange(2, DJANGO_CREATED_FIELD, dataRowCount, 1)
    .setFormulaR1C1(`=IF(OR(RC[${COLUMN_NAME - DJANGO_CREATED_FIELD}]="id", RC[${COLUMN_NAME - DJANGO_CREATED_FIELD}]="uuid", RC[${COLUMN_NAME - DJANGO_CREATED_FIELD}]="created_at", RC[${COLUMN_NAME - DJANGO_CREATED_FIELD}]="updated_at"), TRUE, FALSE)`);

  // Column D: Django created Table (FALSE if app is "core" or "project")
  sheet
    .getRange(2, DJANGO_CREATED_TABLE, dataRowCount, 1)
    .setFormulaR1C1(`=IF(OR(RC[${DJANGO_APP_NAME - DJANGO_CREATED_TABLE}]="core", RC[${DJANGO_APP_NAME - DJANGO_CREATED_TABLE}]="project"), FALSE, TRUE)`);
}

/**
 * Apply checkbox data validation to columns A–E.
 * @param {Sheet} sheet - Target sheet
 * @param {number} dataRowCount - Number of data rows
 */
function applyCheckboxValidation(sheet, dataRowCount) {
  if (dataRowCount === 0) return;

  const checkboxRule = SpreadsheetApp.newDataValidation()
    .requireCheckbox()
    .build();

  sheet.getRange(2, 1, dataRowCount, 5).setDataValidation(checkboxRule);
}

/**
 * Set column widths based on configuration.
 * @param {Sheet} sheet - Target sheet
 */
function formatColumns(sheet) {
  Object.entries(CONFIG.COLUMN_WIDTHS).forEach(([col, width]) => {
    sheet.setColumnWidth(parseInt(col), width);
  });
}

/**
 * Freeze header row.
 * @param {Sheet} sheet - Target sheet
 */
function freezeHeaderRow(sheet) {
  sheet.setFrozenRows(1);
}

/**
 * Hide helper columns (D, F, G).
 * @param {Sheet} sheet - Target sheet
 */
function hideHelperColumns(sheet) {
  sheet.hideColumns(CONFIG.COLUMNS.DJANGO_CREATED_TABLE, 1);
  sheet.hideColumns(CONFIG.COLUMNS.DJANGO_APP_NAME, 2);
}

/**
 * Apply background color to formula columns and Django created fields.
 * @param {Sheet} sheet - Target sheet
 * @param {number} dataRowCount - Number of data rows
 */
function applyBackgroundColors(sheet, dataRowCount) {
  if (dataRowCount === 0) return;

  const { DJANGO_CREATED_TABLE, DJANGO_CREATED_FIELD, TABLE_NAME_PREFIX, IS_NULLABLE } = CONFIG.COLUMNS;

  // Columns D-E (user input formulas)
  sheet.getRange(2, DJANGO_CREATED_TABLE, dataRowCount, 2).setBackground(CONFIG.LIGHT_GRAY);

  // Columns H-K (derived data)
  sheet.getRange(2, TABLE_NAME_PREFIX, dataRowCount, IS_NULLABLE - TABLE_NAME_PREFIX + 1)
    .setBackground(CONFIG.LIGHT_GRAY);

  // Color entire rows light gray if Django created field (column E = TRUE)
  const dataRange = sheet.getRange(2, 1, dataRowCount, CONFIG.HEADERS.length);
  const values = dataRange.getValues();

  values.forEach((row, rowIndex) => {
    const isDjangoCreatedField = row[DJANGO_CREATED_FIELD - 1]; // Column E (index 4)

    if (isDjangoCreatedField === true || isDjangoCreatedField === 'TRUE') {
      sheet.getRange(rowIndex + 2, 1, 1, CONFIG.HEADERS.length)
        .setBackground(CONFIG.LIGHT_GRAY2);
    }
  });
}

/**
 * Apply filter and hide TRUE values in column D.
 * @param {Sheet} sheet - Target sheet
 * @param {number} dataRowCount - Number of data rows
 */
function applyFilter(sheet, dataRowCount) {
  if (dataRowCount === 0) return;

  const filterRange = sheet.getRange(1, 1, dataRowCount + 1, CONFIG.HEADERS.length);
  const filter = filterRange.createFilter();

  const criteria = SpreadsheetApp.newFilterCriteria()
    .setHiddenValues(['TRUE'])
    .build();
  filter.setColumnFilterCriteria(CONFIG.COLUMNS.DJANGO_CREATED_TABLE, criteria);
}

// ═══════════════════════════════════════════════════════════════════════════
// UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Show alert dialog to user.
 * @param {string} message - Alert message
 */
function alertUser(message) {
  SpreadsheetApp.getUi().alert(message);
}

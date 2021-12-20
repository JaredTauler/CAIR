function TableFormat (data) {
    // let data = Object.entries(data["ticket"])
    let table_id = "#ReportTable"
    return TabulatorColumns["ticket"](table_id, data)
}

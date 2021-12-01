function TableFormat (data) {
    let ticket = Object.entries(data["ticket"])
    return new Tabulator("#ReportTable", {
        data: ticket,
        columns: [
            // DATE
            {
                title:
                    "Date", field: "1", sorter: "string",
                    formatter: function (cell) {
                        let field = cell.getValue()[0]
                        let d = new Date(field)
                        return localedate(d)
                    }
            },
            // ACTION
            {
                title: "Interaction", field: "1", sorter: "string",
                formatter: function (cell) {
                    let field = cell.getValue()[1]
                    return data["action"][field][0]
                }
            },
            // INFO
            {
                title: "Additional Info", field: "1", sorter: "string",
                formatter: function (cell) {
                    let field = cell.getValue()[2]
                    // Info is a string, unhashable.
                    return field
                }
            },
            // WORKER FULL NAME (for display)
            {
                title: "Worker", field: "1", sorter: "string", width: 200, download: false,
                formatter: function (cell) {
                    let field = cell.getValue()[3]
                    var fname = data["user"][field][0]
                    var lname = data["user"][field][1]
                    return title(fname) + " " + title(lname)
                }
            },
            // WORKER (for export)
            {
                title: "First Name", field: "1", visible: false, download: true,
                formatter: function (cell) {
                    let field = cell.getValue()[3]
                    return data["user"][field][0]
                }
            },
            {
                title: "Last Name", field: "1", visible: false, download: true,
                formatter: function (cell) {
                    let field = cell.getValue()[3]
                    return data["user"][field][1]
                }
            },
        ],

    });
}

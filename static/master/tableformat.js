function TableFormat (data) {
    return new Tabulator("#ReportTable", {
        data: data,
        columns: [
            {
                title: "Date", field: "date", sorter: "string",
                formatter: function (cell) {
                    let row = cell.getRow().getData();
                    let d = new Date(row["date"])
                    let s = d.toLocaleDateString('en-US', {timeZone: 'UTC'})
                    return s
                }, download:false
            },
            {title: "Interaction", field: "action", sorter: "string"},
            {title: "Additional Info", field: "info", sorter: "string"},
            {
                title: "Worker", field: "name", sorter: "string", width: 200,
                formatter: function (cell) {
                    let row = cell.getRow().getData();
                    return title(row["user_fname"]) + " " + title(row["user_lname"]);
                }, download: false
            },

            {title: "First Name", field: "user_fname", visible: false, download: true},
            {title: "Last Name", field: "user_lname", visible: false, download: true},
            {title: "Worker ID", field: "user_id", visible: false, download: true},
        ],

    });
}

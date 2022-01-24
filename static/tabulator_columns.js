function TableForTabul(source) {
    let arr = []
    for (let row in source["main"]) { // The Rows
        let currow = source["main"][row]

        let objrow = {}
        for (let i in currow) {
            objrow[i.toString()] = currow[i] // strings rather than indexs, tabulators fault!
        }
        arr.push(objrow)
    }
    return arr
}
const TabulatorColumns = {
    "ticket": function (table_id, table) {
        let join = table["join"]
        return new Tabulator(table_id, {
            data: TableForTabul(table),
            columns: [

                // DATE
                {
                    title: "Date", field: "date", sorter: "string",
                    mutator: function (value, data, type, params, component) {
                        let d = new Date(data[0])
                        return localedate(d)
                    }
                },
                // ACTION
                {
                    title: "Interaction", field: "action", sorter: "string",
                    mutator: function (value, data, type, params, component) {
                        return join["action"][data[1]][0];
                    }
                },
                // INFO
                {
                    title: "Additional Info", field: "info", sorter: "string",
                    mutator: function (value, data, type, params, component) {
                        return data[2];
                    }
                },
                // WORKER FULL NAME (for display)
                {
                    title: "Worker", field: "workerfullname", sorter: "string", width: 200, download: false,
                    mutator: function (value, data, type, params, component) {
                        return title(join["user"][data[3]][0]) + " " + title(join["user"][data[3]][1])
                    }
                },
                // WORKER (for export)
                {
                    title: "Worker First Name", field: "workerfirstname", visible: false, download: true,
                    mutator: function (value, data, type, params, component) {
                        return join["user"][data[3]][0];
                    }
                },
                {
                    title: "Worker Last Name", field: "workerlastname", visible: false, download: true,
                    mutator: function (value, data, type, params, component) {
                        return join["user"][data[3]][1];
                    }
                },
                // STUDENT FULL NAME (for display)
                {
                    title: "Student", field: "studentfullname", sorter: "string", width: 200, download: false,
                    mutator: function (value, data, type, params, component) {
                        return title(join["student"][data[4]][0]) + " " + title(join["student"][data[4]][1])
                    }
                },
                // STUDENT (for export)
                {
                    title: "Student First Name", field: "studentfirstname", visible: false, download: true,
                    mutator: function (value, data, type, params, component) {
                        return join["student"][data[4]][0];
                    }
                },
                {
                    title: "Student Last Name", field: "studentlastname", visible: false, download: true,
                    mutator: function (value, data, type, params, component) {
                        return join["student"][data[4]][1];
                    }
                },
            ],
        });
    }
}

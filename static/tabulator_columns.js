const TabulatorColumns = {
    "ticket": function (table_id, data) {
        let arr = Object.entries(data["ticket"])
        if (isMobile) {
            return new Tabulator(table_id, {
                data: arr,
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
                    // STUDENT FULL NAME (for display)
                    {
                        title: "Student", field: "1", sorter: "string", width: 200, download: false,
                        formatter: function (cell) {
                            let field = cell.getValue()[4]
                            console.log(data["student"])
                            console.log(field)
                            var fname = data["student"][field][0]
                            var lname = data["student"][field][1]
                            return title(fname) + " " + title(lname)
                        }
                    },
                    // STUDENT (for export)
                    {
                        title: "Student First Name", field: "1", visible: false, download: true,
                        formatter: function (cell) {
                            let field = cell.getValue()[4]
                            return data["student"][field][0]
                        }
                    },
                    {
                        title: "Student Last Name", field: "1", visible: false, download: true,
                        formatter: function (cell) {
                            let field = cell.getValue()[4]
                            return data["student"][field][1]
                        }
                    },
                ],
            });
        }
        else {
            return new Tabulator(table_id, {
                data: arr,
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
                        title: "Worker First Name", field: "1", visible: false, download: true,
                        formatter: function (cell) {
                            let field = cell.getValue()[3]
                            return data["user"][field][0]
                        }
                    },
                    {
                        title: "Worker Last Name", field: "1", visible: false, download: true,
                        formatter: function (cell) {
                            let field = cell.getValue()[3]
                            return data["user"][field][1]
                        }
                    },
                    // STUDENT FULL NAME (for display)
                    {
                        title: "Student", field: "1", sorter: "string", width: 200, download: false,
                        formatter: function (cell) {
                            let field = cell.getValue()[4]
                            var fname = data["student"][field][0]
                            var lname = data["student"][field][1]
                            return title(fname) + " " + title(lname)
                        }
                    },
                    // STUDENT (for export)
                    {
                        title: "Student First Name", field: "1", visible: false, download: true,
                        formatter: function (cell) {
                            let field = cell.getValue()[4]
                            return data["student"][field][0]
                        }
                    },
                    {
                        title: "Student Last Name", field: "1", visible: false, download: true,
                        formatter: function (cell) {
                            let field = cell.getValue()[4]
                            return data["student"][field][1]
                        }
                    },
                ],
            });
        }
    }
}

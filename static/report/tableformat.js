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

function TableFormat (choice, table) {
    let table_id = "#ReportTable"
    if (["user", "student"].includes(choice)) {
        return TabulatorColumns["ticket"](table_id, table)
    }
    else if (choice === "action_average") {
        return new Tabulator(table_id, {
            data: TableForTabul(table),
            columns: [
                {
                    title: "Average number of days a ticket is open", field: "average",
                    mutator: function (value, data, type, params, component) {
                        return data[0]
                    }, download: true
                },
            ],
        });
    }
    else if (choice === "action_type") {
        return new Tabulator(table_id, {
            data: TableForTabul(table),
            columns: [
                {
                    title: "Interaction Type", field: "action_type", sorter: "string", width: 200,
                    mutator: function (value, data, type, params, component) {

                        return VALUES["drop"]["action_type"][data[0]][0]
                    }, download: true
                },
                {
                    title: "Total", field: "total", sorter: "string", width: 200,
                    mutator: function (value, data, type, params, component) {
                        return data[1]
                    }, download: true
                },
            ],
        });
    }
    else if (choice === "name") {
        return new Tabulator(table_id, {
            data: TableForTabul(table),
            columns: [
                {
                    title: "Student", field: "name", sorter: "string", width: 200,
                    formatter: function (cell) {
                        let data = cell.getRow().getData();
                        return title(data[1]) + " " + title(data[2]);
                    }, download: false
                },
                {
                    title:"First Name", field: "fname", visible:false, download:true,
                    mutator: function (value, data, type, params, component) {
                        return data[2]
                    }
                },
                {
                    title:"Last Name", field: "lname", visible:false, download:true,
                    mutator: function (value, data, type, params, component) {
                        return data[2]
                    }
                },
                {
                    title:"School", field:"school", visible:true, download:true,
                    mutator: function (value, data, type, params, component) {
                        return VALUES["man"]["school"][data[3]][0];
                    }
                },
            ],

        });
    }
    else if (choice === "school_percent") {
         if (EntryDrop.value === "all") {
             return new Tabulator(table_id, {
                data: TableForTabul(table),
                columns: [
                    {
                        title:"School", field:"school", visible:true, download:true,
                        mutator: function (value, data, type, params, component) {
                            return VALUES["man"]["school"][data[0]][0];
                        }
                    },
                    {
                        title:"Total", field: "total", download:true,
                        mutator: function (value, data, type, params, component) {
                            return data[1]
                        }
                    },
                    {
                        title:"Percent", field: "percent", download:true,
                        mutator: function (value, data, type, params, component) {
                            let total = 0
                            for (let i in table["main"]) {
                                total += table["main"][i][1]
                            }
                            let x = data[1]/total
                            x = x * 100
                            x = Math.round(x)
                            x = x.toString(10) + "%"
                            return x

                        }
                    },
                ],

             });
         } else {
             return new Tabulator(table_id, {
                data: TableForTabul(table),
                columns: [
                    {
                        title:"Action", field:"action", visible:true, download:true,
                        mutator: function (value, data, type, params, component) {
                            console.log(VALUES)
                            return VALUES["drop"]["action_type"][data[0]][0];
                        }
                    },
                    {
                        title:"Total", field: "total", download:true,
                        mutator: function (value, data, type, params, component) {
                            return data[1]
                        }
                    },
                    {
                        title:"Percent", field: "percent", download:true,
                        mutator: function (value, data, type, params, component) {
                            let total = 0
                            for (let i in table["main"]) {
                                total += table["main"][i][1]
                            }
                            let x = data[1]/total
                            x = x * 100
                            x = Math.round(x)
                            x = x.toString(10) + "%"
                            return x

                        }
                    },
                ],

             });
         }
    }

}

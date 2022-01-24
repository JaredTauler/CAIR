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
    else if (choice === "action") {
        console.log(table)
        return new Tabulator(table_id, {
            data: TableForTabul(table),
            columns: [
                {
                    title: "Interaction Type", field: "action", sorter: "string", width: 200,
                    mutator: function (value, data, type, params, component) {

                        return VALUES["drop"]["action"][data[0]][0]
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
        console.log(table)
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
                        return table["join"]["schools"][data[3]][0];
                    }
                },
            ],

        });
    }

}

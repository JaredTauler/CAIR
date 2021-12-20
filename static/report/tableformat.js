function TableFormat (choice, data) {
    console.log(data)
    let table_id = "#ReportTable"
    if (["user", "student"].includes(choice)) {
        return TabulatorColumns["ticket"](table_id, data)
    }
    else if (choice === "name") {
        let arr = Object.entries(data["man"])
        return new Tabulator(table_id, {
            data: arr,
            columns: [
                {
                    title: "Student", field: "1", sorter: "string", width: 200,
                    formatter: function (cell) {
                        let field = cell.getValue()
                        return title(field[1]) + " " + title(field[2]);
                    }, download: false
                },

                {
                    title:"First Name", field:"1", visible:false, download:true,
                    formatter: function (cell) {
                        let field = cell.getValue()
                        return field[1]
                    }
                },
                {
                    title:"Last Name", field:"1", visible:false, download:true,
                    formatter: function (cell) {
                        let field = cell.getValue()
                        return field[2]
                    }
                },
                {
                    title:"School", field:"1", visible:true, download:true,
                    formatter: function (cell) {
                        let field = cell.getValue()
                        return data["school"][field[3]][0]
                    }
                },
            ],

        });
    }

}

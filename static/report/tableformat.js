function TableFormat (choice, data) {
    if (choice === "name") {
        return new Tabulator("#ReportTable", {
            data: data,
            columns: [
                {
                    title: "Student", field: "name", sorter: "string", width: 200,
                    formatter: function (cell) {
                        let row = cell.getRow().getData();
                        return title(row["fname"]) + " " + title(row["lname"]);
                    }, download: false
                },

                {title:"First Name", field:"fname", visible:false, download:true},
                {title:"Last Name", field:"lname", visible:false, download:true},

                {
                    title: "Home School", field: "shortname", sorter: "string",
                }
            ],

        });
    }

    else if (choice === "user") {
        return new Tabulator("#ReportTable", {
            data: data,
            columns: [
                {
                    title: "User", field: "user", sorter: "string", width: 200,
                    formatter: function (cell) {
                        let row = cell.getRow().getData();
                        return title(row["user_fname"]) + " " + title(row["user_lname"]);
                    }, download:false
                },
                {title:"User First Name", field:"user_fname", visible:false, download:true},
                {title:"User Last Name", field:"user_lname", visible:false, download:true},
                {
                    title: "Student", field: "student", sorter: "string",
                    formatter: function (cell) {
                        let row = cell.getRow().getData();
                        return title(row["student_fname"]) + " " + title(row["student_lname"]);
                    }, download:false
                },
                {title:"Student First Name", field:"student_fname", visible:false, download:true},
                {title:"Student Last Name", field:"student_lname", visible:false, download:true},

                {
                    title: "Date", field: "date", sorter: "string",
                    formatter: function (cell) {
                        let row = cell.getRow().getData();
                        let d = new Date(row["date"])
                        let s = d.toLocaleDateString('en-US', {timeZone: 'UTC'})
                        return s
                    }, download:false
                },
                {title:"Date", field:"date", visible:false, download:true},
                {
                    title: "Type", field: "type", sorter: "string",
                }
            ]
        });
    }

    else if (choice === "student") {
        let columns = [
            {
                title: "Student", field: "name", sorter: "string", width: 200,
                formatter: function (cell) {
                    let row = cell.getRow().getData();
                    return title(row["fname"]) + " " + title(row["lname"]);
                }, download: false
            },

            {title:"First Name", field:"fname", visible:false, download:true},
            {title:"Last Name", field:"lname", visible:false, download:true},

            {
                title: "Date", field: "date", sorter: "string",
                formatter: function (cell) {
                    let row = cell.getRow().getData();
                    let d = new Date(row["date"])
                    let s = d.toLocaleDateString('en-US', {timeZone: 'UTC'})
                    return s
                },
            },
            {
                title: "Type", field: "type", sorter: "string",
            }
        ]
        if (isMobile === false) {
            columns += [
                {
                    //FIXME finish this!
                }
            ]
        }
        return new Tabulator("#ReportTable", {
            data: data,
            columns: columns
        });
    }
}

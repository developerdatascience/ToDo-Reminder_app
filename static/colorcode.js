document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('#tasks-list tr');

    rows.forEach(row=> {

        const statusCell = row.querySelector("#status_code");
        if (statusCell) {
            switch (statusCell.textContent.trim()) {
                case "Completed":
                    statusCell.style.backgroundColor = "green";
                    statusCell.style.color = "white";
                    break;
                case "In Progress":
                    statusCell.style.backgroundColor = "orange";
                    statusCell.style.color = "white";
                    break;
                case "Pending":
                    statusCell.style.backgroundColor = "red";
                    statusCell.style.color = "white";
                    break;
                default:
                    statusCell.style.backgroundColor = "gray";
                    statusCell.style.color = "white";  
            }
        }
    })
});
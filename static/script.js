function openAddDialog() {
    console.log("Opening add dialog"); // Debug statement
    document.querySelector('#add_dialog')?.showModal();
}

function closeAddDialog() {
    document.querySelector('#add_dialog')?.close();
}

function openEditDialog() {

    document.querySelector('#edit_dialog')?.showModal();
    //new code
}

function closeEditDialog() {
    document.querySelector('#edit_dialog')?.close();
}

function openAddAttendanceDialog() {
    document.querySelector('#add_attendance_dialog')?.showModal();
}

function closeAddAttendanceDialog() {
    document.querySelector('#add_attendance_dialog')?.close();
}

function printReport() {
    console.log("Opening print dialog");
    window.print()
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.search-form').forEach(searchForm => {
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const input = searchForm.search,
                searchData = input.value.toLowerCase(),
                record = document.querySelectorAll(searchForm.dataset.searchRecord);

            record.forEach(tr => {

                if (tr.innerText.toLowerCase().indexOf(searchData) > -1) {
                    tr.style.display = searchForm.dataset.style ?? 'table-row';
                } else
                    tr.style.display = 'none';
            })
        })
    })
})

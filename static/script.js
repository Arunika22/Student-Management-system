function changeClass(e) {
    const value = e.target.value;
    const url = new URL(window.location.href);

    url.searchParams.set('class', value);

    window.location.href = url.toString();
}

function openAddDialog() {
    document.querySelector('#add_dialog')?.showModal();
}

function closeAddDialog() {
    document.querySelector('#add_dialog')?.close();
}

function openEditDialog(e) {
    const dialog = document.querySelector('#edit_dialog');
    dialog?.showModal();

    const form = dialog?.querySelector('form');

    if(!form) return
    console.log(e.target.dataset.name)
    const data = JSON.parse(e.target.dataset.name);
    console.log(data)


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

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.search-form').forEach(searchForm => {
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const input = searchForm.search,
                searchData = input.value,
                record = document.querySelector(searchForm.dataset.searchRecord);
            record.querySelectorAll('tr').forEach(tr => {
                
                if(tr.innerText.indexOf(searchData) > -1) {
                    tr.style.display = 'table-row';
                }else 
                    tr.style.display = 'none';
            })
        })
    })
})
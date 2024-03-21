function changeClass(e) {
    const value = e.target.value;
    const url = new URL(window.location.href);

    url.searchParams.set('class', value);

    window.location.href = url.toString();
}

// function openAddDialog() {
//     document.querySelector('#add_dialog')?.showModal();
// }

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


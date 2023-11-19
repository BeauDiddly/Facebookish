bioContainer = document.querySelector('bio')
editButton = document.getElementById('edit-bio')
updateBioForm = document.getElementById('bio-form')

editButton.onclick = () => {
    updateBioForm.classList.toggle('hidden-update-bio-form')
}
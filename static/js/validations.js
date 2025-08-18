// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();

// supresson docteur
function setDeleteUrl(doctorId) {
  const url = `/admin/supprimer_docteur/${doctorId}`;
  const confirmBtn = document.getElementById("confirmDeleteBtn");
  if (confirmBtn) {
    confirmBtn.setAttribute("href", url);
  }
}

//supresion admin
function updateDeleteLink(button) {
  const adminId = button.getAttribute("data-id");
  const deleteUrl = `/admin/supprimer/${adminId}`; // Chemin exact selon ta route Flask
  document.getElementById("confirmDeleteBtn").setAttribute("href", deleteUrl);
}

// supresion patient
function updateDeleteLinkPatient(button) {
  const patientId = button.getAttribute("data-id");
  const deleteUrl = `/admin/patient/supprimer/${patientId}`; // Assure-toi que cette route existe en Flask
  document.getElementById("confirmDeleteBtn").setAttribute("href", deleteUrl);
}

// supression secretaire medical
function updateDeleteLinkSecretaire(button) {
  const secretaireId = button.getAttribute("data-id");
  const deleteUrl = `/admin/secretaire/supprimer/${secretaireId}`;
  document.getElementById("confirmDeleteBtn").setAttribute("href", deleteUrl);
}

// supresion admission
function updateDeleteLinkAdmission(button) {
  const admissionId = button.getAttribute("data-id");
  const deleteUrl = `/admin/admission/supprimer/${admissionId}`;
  const confirmBtn = document.getElementById("confirmDeleteBtn");
  if (confirmBtn) {
    confirmBtn.setAttribute("href", deleteUrl);
  }
}

// suppression sortie
function updateDeleteLinkSortie(button) {
  const sortieId = button.getAttribute("data-id");
  // URL correcte selon ta route Flask
  const deleteUrl = `/secretaire/sortie/supprimer/${sortieId}`;
  const confirmBtn = document.getElementById("confirmDeleteBtn");
  if (confirmBtn) {
    confirmBtn.setAttribute("href", deleteUrl);
  }
}

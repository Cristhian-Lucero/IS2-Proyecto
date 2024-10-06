const draggables = document.querySelectorAll(".task"); // todos los elementos arrastables
const droppables = document.querySelectorAll(".swim-lane"); // donde se pueden soltar los arrastables

draggables.forEach((task) => {
  task.addEventListener("dragstart", () => { // evento: añade la clase cuando se esta arrastrando
    task.classList.add("is-dragging");
  });

  task.addEventListener("dragend", () => { // evento: elimina la clase cuando lo suelta
    task.classList.remove("is-dragging");

    // Obtener la columna donde fue soltado el elemento
    const newState = task.parentElement.getAttribute("data-state"); // Identifica la nueva columna (estado)

    // Enviar una solicitud AJAX para actualizar el estado en la base de datos
    const taskId = task.getAttribute("data-id"); // Obtener el ID de la tarea

    // Aquí está la solicitud fetch que actualiza el estado de la tarea en el servidor
    fetch(`/Tablero/update_task_state/${taskId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),  // Token CSRF para seguridad
      },
      body: JSON.stringify({ estado: newState }), // Enviar el nuevo estado en el cuerpo de la solicitud
    })
    .then((response) => {
      if (response.ok) {
        console.log("Estado actualizado correctamente");
      } else {
        console.error("Error al actualizar el estado");
      }
    });
  });
});

droppables.forEach((zone) => {
  zone.addEventListener("dragover", (e) => { // para cada zona donde puede soltar el objeto
    e.preventDefault(); // permite que el objeto arrastrado pueda ser soltado
    const curTask = document.querySelector(".is-dragging"); // Se selecciona el elemento que está siendo arrastrado actualmente
    zone.appendChild(curTask); // Se mueve el elemento arrastrado a la zona de destino
  });
});

// Obtener el token CSRF para la solicitud
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

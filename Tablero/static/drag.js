const draggables = document.querySelectorAll(".task"); // todos los elementos arrastables
const droppables = document.querySelectorAll(".swim-lane"); // donde se pueden soltar los arrastables

draggables.forEach((task) => {
  task.addEventListener("dragstart", () => { // evento: añade la clase cuando se esta arrastrando
    task.classList.add("is-dragging");
  });
  task.addEventListener("dragend", () => { // evento: elimina la clase cuando lo suelta
    task.classList.remove("is-dragging");
  });
});

droppables.forEach((zone) => {
  zone.addEventListener("dragover", (e) => { // para cada zona donde puede soltar el objeto
    e.preventDefault(); // permite que el objeto arrastrado pueda ser soltado

    const bottomTask = insertAboveTask(zone, e.clientY); // insertAboveTask: Esta función se llama para determinar cuál es la tarea que se encuentra justo debajo del cursor del mouse, basándose en la posición clientY del mouse.
    const curTask = document.querySelector(".is-dragging"); // Se selecciona el elemento que está siendo arrastrado actualmente con document.querySelector(".is-dragging").

    if (!bottomTask) { // si es nulo se agrega al final, sino se inserta antes
      zone.appendChild(curTask);
    } else {
      zone.insertBefore(curTask, bottomTask);
    }
  });
});

const insertAboveTask = (zone, mouseY) => { // Determina la zona mas cercana al mouse
  const els = zone.querySelectorAll(".task:not(.is-dragging)"); //Filtra todos los task dentro de la zona que no están siendo arrastradas (.task:not(.is-dragging)).

  let closestTask = null;
  let closestOffset = Number.NEGATIVE_INFINITY;

  els.forEach((task) => {
    const { top } = task.getBoundingClientRect(); // Para cada task dentro de la zona, calcula la distancia vertical entre la parte superior del task y la posición del mouse.

    const offset = mouseY - top;

    if (offset < 0 && offset > closestOffset) { //Si la distancia (offset) es negativa (el mouse está por encima del task), y esta distancia es la más cercana encontrada hasta el momento, se actualiza closestTask para que sea el task más cercana al cursor.
      closestOffset = offset;
      closestTask = task;
    }
  });

  return closestTask;
};

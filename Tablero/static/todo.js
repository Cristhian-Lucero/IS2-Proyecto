const form = document.getElementById("todo-form"); // donde se puede agregar task
const input = document.getElementById("todo-input"); //
const todoLane = document.getElementById("todo-lane"); // el contenedor (<div>)

form.addEventListener("submit", (e) => {
  e.preventDefault(); //
  const value = input.value; //

  if (!value) return;

  const newTask = document.createElement("p"); // crea un nuevo elemento
  newTask.classList.add("task"); // le dice que es un task (un elemento arrastrable)
  newTask.setAttribute("draggable", "true"); // le dice que puede ser arrastrable
  newTask.innerText = value; //

  newTask.addEventListener("dragstart", () => { // Se activa cuando el usuario empieza a arrastrar el elemento. Durante este evento, se añade la clase "is-dragging" al elemento,
    newTask.classList.add("is-dragging");
  });

  newTask.addEventListener("dragend", () => { // Se activa cuando el usuario deja de arrastrar el elemento. Se elimina la clase "is-dragging".
    newTask.classList.remove("is-dragging");
  });

  todoLane.appendChild(newTask); //Una vez que se ha creado y configurado la nueva tarea, se añade al contenedor todoLane, lo que significa que el nuevo párrafo se mostrará dentro del contenedor de tareas.

  input.value = ""; //
});

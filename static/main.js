const form = document.querySelector('#form');
const ageError = document.querySelector('#age-error');
const emailError = document.querySelector('#email-error');
const passwordError = document.querySelector('#password-error');


let users = []
let editing = false
let userid = null 


const emailRegex =/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
const passwordRegex = /^.{4,12}$/



window.addEventListener('DOMContentLoaded', async () => {

  const response = await fetch('/api/users')
  const data = await response.json()
  users = data
  renderUser(users)

});

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = form['username'].value;
  const surname = form['surname'].value;
  const age = form['age'].value;
  const email = form['email'].value;
  const password = form['password'].value;

  if (!emailRegex.test(email)) {
    emailError.textContent = 'Estructura no esperada';
    return;
  } else {
    emailError.textContent = ''; // Borra el mensaje de error si el correo es válido
  }

  if (!passwordRegex.test(password)) {
    passwordError.textContent = 'Estructura no esperada';
    return;
  } else {
    passwordError.textContent = ''; // Borra el mensaje de error si el correo es válido
  }

  if (isNaN(parseInt(age))) {
    ageError.textContent = 'Debe ingresar edad(numero)';
    return
  } else if (parseInt(age) < 18) {
    ageError.textContent = 'Debe ser mayor a 18 años para registrarse ';
    return
  }
  else{
    ageError.textContent = '';
  }

  if (!editing) {

  const response = await fetch('/api/users',{
    method:'POST',
    headers:{
      'Content-Type': 'application/json'
    },

    body: JSON.stringify({
      username,
      surname,
      age,
      email,
      password
    })
  });

  const data = await response.json()
  users.push(data)

  } else {
    const response = await fetch(`/api/users/${userid}` ,{
      method: 'PUT', 
      headers:{
        'Content-Type': 'application/json'
      },  
      body: JSON.stringify({
        username,
        surname,
        age,
        email,
        password
      })
    })

    const updateUser = await response.json()
    
    users = users.map(user => user.id === updateUser.id ? updateUser : user )

    editing = false 
    userid = null
  }

  renderUser(users)

  form.reset()

});

function renderUser(users) {
  const Userlist = document.querySelector('#userlist')
  Userlist.innerHTML = '';

  users.forEach(user => {
    const Useritems = document.createElement('li')
    Useritems.innerHTML = `
      <header class=button-type>
        <h3>${user.username}</h3>
        <div>
          <button class = "button-delete ">Delete</button>
          <button class = "button-edit " >Edit</button>
        </div>
      </header>
      <p>${user.surname}</p>
      <p>${user.age}</p>
      <p>${user.email}</p>
      <p class= "text-truncate">${user.password}</p>
    `;

    const button_delete = Useritems.querySelector('.button-delete')

    button_delete.addEventListener('click' , async () => {
      
      const responses = await fetch(`/api/users/${user.id}`,{
      method: 'DELETE',

      })

      const data = await responses.json()

      users = users.filter(user => user.id !== data.id)

      renderUser(users)
    })

    const button_edit = Useritems.querySelector('.button-edit')

    button_edit.addEventListener('click' , async () => {
      const response = await fetch(`/api/users/${user.id}`);
      const data = await response.json()
      
      form['username'].value = data.username;
      form['surname'].value = data.surname;
      form['age'].value = data.age;
      form['email'].value = data.email;

      editing = true

      userid = user.id
    })

    Userlist.append(Useritems)
  
  })
};
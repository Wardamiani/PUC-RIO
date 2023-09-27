/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = "http://127.0.0.1:5000/hospede";
  fetch(url, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      data.hospedes.forEach((item) =>
        insertList(item.nome, item.quartos, item.dias, item.valor)
      );
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList();

/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputName, inputQuantity, inputDate, inputPrice) => {
  const formData = new FormData();
  formData.append("nome", inputName);
  formData.append("quartos", inputQuantity);
  formData.append("dias", inputDate);
  formData.append("valor", inputPrice);

  let url = "http://127.0.0.1:5000/hospede";
  fetch(url, {
    method: "post",
    body: formData,
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error:", error);
    });
};

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
};

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName("td")[0].innerHTML;
      if (confirm("Você tem certeza?")) {
        div.remove();
        deleteItem(nomeItem);
        alert("Hóspede removido!");
      }
    };
  }
};

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item);
  let url = "http://127.0.0.1:5000/hospede?nome=" + item;
  fetch(url, {
    method: "delete",
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error:", error);
    });
};

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade, data de estadia e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = () => {
  let inputClient = document.getElementById("newInput").value;
  let inputQuantity = document.getElementById("newQuantity").value;
  let inputDate = document.getElementById("newDate").value;
  let inputPrice = document.getElementById("newPrice").value;

  if (inputClient === "") {
    alert("Escreva o nome de um hóspede!");
  } else if (isNaN(inputQuantity) || isNaN(inputPrice) || isNaN(inputDate)) {
    alert("Quantidade, valor e dias de estadia precisam ser números!");
  } else {
    insertList(inputClient, inputQuantity, inputDate, inputPrice);
    postItem(inputProduct, inputQuantity, inputDate, inputPrice);
    alert("Item adicionado!");
  }
};

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nameClient, quantity, date, price) => {
  var item = [nameClient, quantity, date, price];
  var table = document.getElementById("myTable");
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1));
  document.getElementById("newInput").value = "";
  document.getElementById("newQuantity").value = "";
  document.getElementById("newDate").value = "";
  document.getElementById("newPrice").value = "";

  removeElement();
};

/*
  --------------------------------------------------------------------------------------
  API externa 1 - OpenWeather
  --------------------------------------------------------------------------------------
*/

const apiKey = `acd83b3b3e4f8eb29071ebfe535d7a10`;
const apiUrl = `https://api.openweathermap.org/data/2.5/weather?&lang=pt_br&units=metric&q=`;

const searchBox = document.querySelector(".search input");
const searchBtn = document.querySelector(".search button");
const iconeTempo = document.querySelector(".icone-tempo");
const descElement = document.querySelector(".descricaotempo");

async function checkWeather(cidade) {
  const response = await fetch(apiUrl + cidade + `&appid=${apiKey}`);

  if (response.status == 404) {
    document.querySelector(".error").style.display = "block";
    document.querySelector(".weather").style.display = "none";
  } else {
    const data = await response.json();

    document.querySelector(".cidade").innerHTML = data.name;
    document.querySelector(".temperatura").innerHTML =
      Math.round(data.main.temp) + "ºC";
    document.querySelector(".umidade").innerHTML = data.main.humidity + "%";
    document.querySelector(".vento").innerHTML = data.wind.speed + " Km/h";

    descElement.innerText = data.weather[0].description;

    iconeTempo.setAttribute(
      "src",
      `https://openweathermap.org/img/wn/${data.weather[0].icon}.png`
    );

    document.querySelector(".weather").style.display = "block";
    document.querySelector(".error").style.display = "none";
  }
}

searchBtn.addEventListener("click", () => {
  checkWeather(searchBox.value);
});


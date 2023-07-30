const firebaseConfig = {
  apiKey: "AIzaSyBKEiTRqZrYGQuwmreu4bDiUN9gwe9j1Lk",
  authDomain: "appsec2-8c9a7.firebaseapp.com",
  databaseURL: "https://appsec2-8c9a7-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "appsec2-8c9a7",
  storageBucket: "appsec2-8c9a7.appspot.com",
  messagingSenderId: "548391003458",
  appId: "1:548391003458:web:388e9a31f15c041d3cd4db"

};

firebase.initializeApp(firebaseConfig);
const db = firebase.database();

function renderBlogEntries(data) {
  const blogEntriesDiv = document.getElementById("container2");

  // Create a new div for each blog entry
  data.forEach((entry) => {
    const entryDiv = document.createElement("div");
    entryDiv.classList.add("blog-entry");

    // Add the "name" field
    const nameElement = document.createElement("p");
    nameElement.textContent = entry.name;
    entryDiv.appendChild(nameElement);

    // Add the "blog_title" field
    const titleElement = document.createElement("h5");
    titleElement.textContent = entry.blog_title;
    entryDiv.appendChild(titleElement);

    // Add the "blog_content" field
    const contentElement = document.createElement("p");
    contentElement.textContent = entry.blog_content;
    entryDiv.appendChild(contentElement);

    // Append the entry div to the container
    blogEntriesDiv.appendChild(entryDiv);
  });
}

function loadBlogEntries() {
  db.ref("blog").on("value", (snapshot) => {
    const data = snapshot.val();
    if (data) {
      const dataArray = Object.values(data);
      renderBlogEntries(dataArray);
    }
  });
}

document.addEventListener("DOMContentLoaded", loadBlogEntries);
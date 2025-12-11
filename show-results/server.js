const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");
const { MongoClient } = require("mongodb");

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

// Internal Docker service URLs
const AUTH = "http://auth-service:5000";
const MONGO = "mongodb://mongo-db:27017/";
const DB = "analyticsdb";
const COLL = "metrics";

// Starting point
app.get("/", (req, res) => {
  res.send(`
    <h1>Darcy's Results Page</h1>

    <form method="post" action="/results">
      User:<input name="username"><br>
      Pass:<input name="password" type="password"><br>
      <button>Go</button>
    </form>

    <hr>

    <form method="post" action="/run-analytics">
      <button>Compute Analytics Now</button>
    </form>
  `);
});

// results page attempt
app.post("/results", async (req, res) => {
  try {
    const username = req.body.username;
    const password = req.body.password;

    // Authenticate the user
    const authResponse = await axios.post(AUTH + "/login", {
      username,
      password
    });

    if (authResponse.status !== 200) {
      return res.send("Invalid");
    }

    // Connect to MongoDB
    const client = await MongoClient.connect(MONGO);
    const col = client.db(DB).collection(COLL);

    // get the latest entries
    const latest = await col.findOne({}, { sort: { computed_at: -1 } });
    await client.close();

    if (!latest) {
      return res.send("No analytics");
    }

    // show the result
    return res.send(`
      <h1>Latest</h1>
      Count: ${latest.count}<br>
      Min: ${latest.min}<br>
      Max: ${latest.max}<br>
      Avg: ${latest.avg}
    `);

  } catch (e) {
    return res.send("Error: " + e.message);
  }
});

// run the analytics function
app.post("/run-analytics", async (req, res) => {
  try {
    const result = await axios.post("http://analytics-service:5000/run-once");

    return res.send(`
      <h1>Analytics Computed</h1>
      <pre>${JSON.stringify(result.data, null, 2)}</pre>
      <br>
      <a href="/">Back to Results Page</a>
    `);

  } catch (e) {
    return res.send("Error computing analytics: " + e.message);
  }
});

// Start server
app.listen(3000);

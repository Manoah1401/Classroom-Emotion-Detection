const { plugins } = require("chart.js");

      const personalDetails = {
        Student1: {
          year: 3,
          RegNo: 1001,
        },
        Student2: {
          year: 3,
          RegNo: 1002,
        },
        Student3: {
          year: 3,
          RegNo: 1003,
        },
        Student4: {
          year: 3,
          RegNo: 1004,
        },
        Student5: {
          year: 3,
          RegNo: 1005,
        },
      };

      Chart.defaults.color = '#ecf0f1';
      selectReport('overall');

      async function fetchEmotionalData() {
        const response = await fetch("emotion_occurrence.json");
        const data = await response.json();
        return data;
      }

      async function showIndividualReport(person) {
        const reportsContainer = document.getElementById("reports");
        reportsContainer.innerHTML = "";

        const jsonData = await fetchEmotionalData();

        const personData = Object.entries(jsonData).map(
          ([emotion, values]) => ({ emotion, value: values[person] })
        );

        const highestEmotion = personData.reduce(
          (max, { value, emotion }) => {
            if (value > max.value) {
              return { value, emotion };
            } else {
              return max;
            }
          },
          { value: -Infinity }
        );

        const totalClasses = personData.reduce(
          (acc, { value }) => acc + value,
          0
        );

        personData.forEach(({ value }, index) => {
          personData[index].percentage = ((value / totalClasses) * 100).toFixed(
            2
          );
        });

        const reportDiv = document.createElement("div");
        reportDiv.className = "chart-container";
        reportDiv.innerHTML = `
                <div class="report-header">
                    <h3>${person}'s Emotional Report</h3>
                    <p>Year: ${personalDetails[person].year}</p>
                    <p>Registration Number: ${personalDetails[person].RegNo}</p>
                    <p>Highest Emotion: ${highestEmotion.emotion} (${(
          (highestEmotion.value / totalClasses) *
          100
        ).toFixed(2)}%)</p>
                </div>
                <div class="report-details1">
                    <canvas id="${person}-chart" width="300" height="300"></canvas>
                    <ul class="emotion-list">
                        ${personData
                          .map(
                            ({ emotion, value, percentage }) =>
                              `<li>${emotion}: ${value} (${percentage}%)</li>`
                          )
                          .join("")}
                    </ul>
                </div>
            `;
        reportsContainer.appendChild(reportDiv);

        var ctx = document.getElementById(`${person}-chart`).getContext("2d");
        var myChart = new Chart(ctx, {
          type: "pie",
          data: {
            labels: personData.map(({ emotion }) => emotion),
            datasets: [
              {
                data: personData.map(({ value }) => value),
                backgroundColor: [
                  "rgba(255, 99, 132, 0.5)",
                  "rgba(54, 162, 235, 0.5)",
                  "rgba(255, 206, 86, 0.5)",
                  "rgba(75, 192, 192, 0.5)",
                  "rgba(153, 102, 255, 0.5)",
                  "rgba(255, 159, 64, 0.5)",
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 206, 86, 1)",
                  "rgba(75, 192, 192, 1)",
                  "rgba(153, 102, 255, 1)",
                  "rgba(255, 159, 64, 1)",
                ],
                borderWidth: 1,
              },
            ],
          },
          options: {
            title: {
              display: true,
              text: "Emotional Report",
            },
          },
        });
      }

      async function showOverallReport() {
        const reportsContainer = document.getElementById("reports");
        reportsContainer.innerHTML = "";

        const jsonData = await fetchEmotionalData();

        const totalEmotions = {};
        Object.keys(jsonData).forEach((emotion) => {
          totalEmotions[emotion] = Object.values(jsonData[emotion]).reduce(
            (acc, val) => acc + val,
            0
          );
        });

        const highestEmotion = Object.keys(totalEmotions).reduce(
          (max, emotion) => {
            if (totalEmotions[emotion] > max.value) {
              return { value: totalEmotions[emotion], emotion };
            } else {
              return max;
            }
          },
          { value: -Infinity }
        );

        const totalClasses = Object.values(totalEmotions).reduce(
          (acc, val) => acc + val,
          0
        );

        Object.keys(totalEmotions).forEach((emotion) => {
          totalEmotions[emotion] = (
            (totalEmotions[emotion] / totalClasses) *
            100
          ).toFixed(2);
        });

        const reportDiv = document.createElement("div");
        reportDiv.className = "chart-container";
        reportDiv.innerHTML = `
                <div class="report-header">
                    <h3>Overall Class Report</h3>
                    <p>Highest Emotion: ${highestEmotion.emotion} (${(
          (highestEmotion.value / totalClasses) *
          100
        ).toFixed(2)}%)</p>
                </div>
                <div class="report-details1">
                    <canvas id="overall-chart" width="300" height="300"></canvas>
                    <ul class="emotion-list">
                        ${Object.entries(totalEmotions)
                          .map(
                            ([emotion, percentage]) =>
                              `<li>${emotion}: ${percentage}%</li>`
                          )
                          .join("")}
                    </ul>
                </div>
            `;
        reportsContainer.appendChild(reportDiv);

        var ctx = document.getElementById("overall-chart").getContext("2d");
        var myChart = new Chart(ctx, {
          type: "pie",
          data: {
            labels: Object.keys(totalEmotions),
            datasets: [
              {
                data: Object.values(totalEmotions),
                backgroundColor: [
                  "rgba(255, 99, 132, 0.5)",
                  "rgba(54, 162, 235, 0.5)",
                  "rgba(255, 206, 86, 0.5)",
                  "rgba(75, 192, 192, 0.5)",
                  "rgba(153, 102, 255, 0.5)",
                  "rgba(255, 159, 64, 0.5)",
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 206, 86, 1)",
                  "rgba(75, 192, 192, 1)",
                  "rgba(153, 102, 255, 1)",
                  "rgba(255, 159, 64, 1)",
                ],
                borderWidth: 1,
              },
            ],
          },
          options: {
            title: {
              display: true,
              text: "Overall Class Report",
            },
            plugins: {
              tooltip: {
                  callbacks: {
                      label: function(context) {
                          let label = context.label;
                          
                          let highestScoree = findPersonWithMaxValueForEmotion(jsonData, label);
                          return highestScoree;
                      }
                  }
              }
          }
          },
        });
      }

      function findPersonWithMaxValueForEmotion(jsonData, emotion) {
        // Convert the emotion to lowercase to ensure case-insensitive matching
      
        // Check if the provided emotion exists in the data
        if (!Object.keys(jsonData).includes(emotion)) {
          return emotion;
        }
      
        const emotionData = jsonData[emotion];
        const maxPerson = Object.keys(emotionData).reduce((maxPerson, person) => {
          const value = emotionData[person];
          if (value > emotionData[maxPerson]) {
            return person;
          } else {
            return maxPerson;
          }
        });
      
        return maxPerson;
      }
      function selectReport(value) {
        const reportType = value;
        if (reportType === "individual") {
          document.getElementById("report-person").style.display =
            "block";
          document.getElementById("reports").innerHTML = "";
          showIndividualReport(document.getElementById("report-person").value);
        } else if (reportType === "overall") {
          document.getElementById("report-person").style.display = "none";
          document.getElementById("reports").innerHTML = "";
          showOverallReport();
        }
      }

      function selectPerson() {
        const person = document.getElementById("report-person").value;
        showIndividualReport(person);
      }
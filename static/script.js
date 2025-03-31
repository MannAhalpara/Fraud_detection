

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("transactionForm");

    // Auto-fill timestamp
    function updateTimestamp() {
        const timestampField = document.getElementById("timestamp");
        const now = new Date();
        timestampField.value = now.toISOString().slice(0, 19).replace("T", " "); // Format: YYYY-MM-DD HH:MM:SS
    }

    // Call updateTimestamp() when the page loads
    updateTimestamp();

    // Prevent negative transaction amounts
    document.getElementById("transactionAmount").addEventListener("input", function () {
        if (this.value < 0) {
            this.value = 0;
        }
    });

    // Form submission
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        const transactionID = Math.random().toString(36).substr(2, 9); // Generate random transaction ID
        const senderAccount = document.getElementById("senderAccount").value;
        const receiverAccount = document.getElementById("receiverAccount").value;
        const transactionAmount = document.getElementById("transactionAmount").value;
        const transactionType = document.getElementById("transactionType").value;
        const transactionLocation = document.getElementById("transactionLocation").value;
        const ipAddress = document.getElementById("ipAddress").value;
        const timestamp = document.getElementById("timestamp").value;

        if (!senderAccount || !receiverAccount || !transactionAmount || transactionType === "Select type") {
            alert("Please fill in all required fields.");
            return;
        }

        // Simulating balance & transaction success
        const balance = 10000 - parseFloat(transactionAmount); // Example balance logic
        const transactionSuccess = 1; // Assume success
        const status = "Completed"; // Default status

        // Data to send to backend
        const transactionData = {
            transactionID,
            senderAccount,
            receiverAccount,
            transactionAmount,
            balance,
            ipAddress,
            transactionType,
            transactionSuccess,
            status,
            transactionLocation,
            timestamp
        };

        console.log("Sending data:", transactionData);

        // Sending data to backend (Flask)
        fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(transactionData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Show result from backend
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const emlFileInput = document.getElementById("emlFile");
    const uploadStatus = document.getElementById("upload-status");
    const parsedEmailsTableBody = document.getElementById("parsed-emails-table").getElementsByTagName("tbody")[0];
    const rawEmailsTableBody = document.getElementById("raw-emails-table").getElementsByTagName("tbody")[0];

    const fetchData = () => {
        fetch("/api/v1/parser/get")
            .then(response => response.json())
            .then(data => {
                // Clear existing table data
                parsedEmailsTableBody.innerHTML = '';
                rawEmailsTableBody.innerHTML = '';

                data.parsed_emails.forEach(email => {
                    const row = parsedEmailsTableBody.insertRow();
                    row.insertCell(0).innerText = email.id;
                    row.insertCell(1).innerText = email.from_address;
                    row.insertCell(2).innerText = email.to_address;
                    row.insertCell(3).innerText = email.subject;
                    row.insertCell(4).innerText = new Date(email.date).toLocaleString();
                    row.insertCell(5).innerText = email.sender_ip;
                    row.insertCell(6).innerText = email.ollama_evaluation;
                    row.insertCell(7).innerText = email.raw_email_id;
                });

                data.raw_emails.forEach(email => {
                    const row = rawEmailsTableBody.insertRow();
                    row.insertCell(0).innerText = email.id;
                    row.insertCell(1).innerText = email.raw_content.substring(0, 100) + '...'; // Truncate for display
                    row.insertCell(2).innerText = email.parsed_email_id;
                });
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                uploadStatus.innerHTML = '<div class="alert alert-danger">Error fetching data. See console for details.</div>';
            });
    };

    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (!emlFileInput.files.length) {
            uploadStatus.innerHTML = '<div class="alert alert-warning">Please select a file to upload.</div>';
            return;
        }

        const formData = new FormData();
        formData.append("file", emlFileInput.files[0]);

        uploadStatus.innerHTML = '<div class="alert alert-info">Uploading and analyzing...</div>';

        try {
            const response = await fetch("/api/v1/rules/generate_from_file", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                uploadStatus.innerHTML = '<div class="alert alert-success">File uploaded and analyzed successfully!</div>';
                console.log("Analysis Result:", result);
                fetchData(); // Reload data after successful upload
            } else {
                const errorData = await response.json();
                uploadStatus.innerHTML = `<div class="alert alert-danger">Error: ${errorData.detail || response.statusText}</div>`;
                console.error("Upload failed:", errorData);
            }
        } catch (error) {
            uploadStatus.innerHTML = '<div class="alert alert-danger">Network error or server unreachable.</div>';
            console.error("Network error:", error);
        }
    });

    // Initial data fetch when the page loads
    fetchData();
});
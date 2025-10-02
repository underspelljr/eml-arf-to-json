document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const emlFileInput = document.getElementById("emlFile");
    const uploadStatus = document.getElementById("upload-status");
    const parsedEmailsTableBody = document.getElementById("parsed-emails-table").getElementsByTagName("tbody")[0];
    const rawEmailsTableBody = document.getElementById("raw-emails-table").getElementsByTagName("tbody")[0];

    // Modal elements
    const deleteConfirmationModal = new bootstrap.Modal(document.getElementById('deleteConfirmationModal'));
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    let emailToDeleteId = null;

    const fetchData = () => {
        fetch("/api/v1/parser/get")
            .then(response => response.json())
            .then(data => {
                // Clear existing table data
                parsedEmailsTableBody.innerHTML = '';
                rawEmailsTableBody.innerHTML = '';

                data.parsed_emails.forEach(email => {
                    const row = parsedEmailsTableBody.insertRow();
                    row.id = `parsed-email-${email.id}`;
                    row.insertCell(0).innerText = email.id;
                    row.insertCell(1).innerText = email.from_address;
                    row.insertCell(2).innerText = email.to_address;
                    row.insertCell(3).innerText = email.subject;
                    row.insertCell(4).innerText = new Date(email.date).toLocaleString();
                    row.insertCell(5).innerText = email.sender_ip;
                    row.insertCell(6).innerText = email.ollama_evaluation;
                    const rawEmailIdCell = row.insertCell(7);
                    if (email.raw_email_id) {
                        const rawEmailLink = document.createElement('a');
                        rawEmailLink.href = `#raw-email-${email.raw_email_id}`;
                        rawEmailLink.innerText = email.raw_email_id;
                        rawEmailLink.addEventListener('click', (e) => {
                            e.preventDefault();
                            scrollToElement(`raw-email-${email.raw_email_id}`);
                        });
                        rawEmailIdCell.appendChild(rawEmailLink);
                    } else {
                        rawEmailIdCell.innerText = 'N/A';
                    }
                    const actionsCell = row.insertCell(8);
                    const deleteIcon = document.createElement('i');
                    deleteIcon.classList.add('fas', 'fa-trash-alt', 'text-danger');
                    deleteIcon.style.cursor = 'pointer';
                    deleteIcon.addEventListener('click', () => {
                        emailToDeleteId = email.id;
                        deleteConfirmationModal.show();
                    });
                    actionsCell.appendChild(deleteIcon);
                });

                data.raw_emails.forEach(email => {
                    const row = rawEmailsTableBody.insertRow();
                    row.id = `raw-email-${email.id}`;
                    row.insertCell(0).innerText = email.id;
                    row.insertCell(1).innerText = email.raw_content.substring(0, 100) + '...'; // Truncate for display
                    const parsedEmailIdCell = row.insertCell(2);
                    if (email.parsed_email_id) {
                        const parsedEmailLink = document.createElement('a');
                        parsedEmailLink.href = `#parsed-email-${email.parsed_email_id}`;
                        parsedEmailLink.innerText = email.parsed_email_id;
                        parsedEmailLink.addEventListener('click', (e) => {
                            e.preventDefault();
                            scrollToElement(`parsed-email-${email.parsed_email_id}`);
                        });
                        parsedEmailIdCell.appendChild(parsedEmailLink);
                    } else {
                        parsedEmailIdCell.innerText = 'N/A';
                    }
                    const actionsCell = row.insertCell(3);
                    // Raw emails are deleted when parsed emails are deleted, so no separate delete for raw_emails here
                    actionsCell.innerText = "N/A";
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
                if (result.error) {
                    alert("Ollama analysis failed, but the file was still saved. Error: " + result.details);
                }
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

    confirmDeleteBtn.addEventListener('click', async () => {
        if (emailToDeleteId !== null) {
            try {
                const response = await fetch(`/api/v1/parser/emails/${emailToDeleteId}`, {
                    method: 'DELETE',
                });

                if (response.ok) {
                    uploadStatus.innerHTML = '<div class="alert alert-success">Email deleted successfully!</div>';
                    fetchData(); // Refresh the table
                } else {
                    const errorData = await response.json();
                    uploadStatus.innerHTML = `<div class="alert alert-danger">Error deleting email: ${errorData.detail || response.statusText}</div>`;
                    console.error("Delete failed:", errorData);
                }
            } catch (error) {
                uploadStatus.innerHTML = '<div class="alert alert-danger">Network error during deletion.</div>';
                console.error("Network error during deletion:", error);
            } finally {
                deleteConfirmationModal.hide();
                emailToDeleteId = null;
            }
        }
    });

    // Initial data fetch when the page loads
    fetchData();
});

// Chat functionality
function formatResponse(response) {
    // Split response into paragraphs
    const paragraphs = response.split('\n\n');
    let formattedHtml = '';
    
    paragraphs.forEach((paragraph, index) => {
        // Check if paragraph is a numbered list
        if (paragraph.match(/^\d+\./m)) {
            const items = paragraph.split('\n');
            formattedHtml += '<ol class="numbered-list">';
            items.forEach(item => {
                if (item.trim()) {
                    // Remove the number and dot from the beginning
                    const cleanItem = item.replace(/^\d+\.\s*/, '');
                    formattedHtml += `<li>${cleanItem}</li>`;
                }
            });
            formattedHtml += '</ol>';
        } else {
            formattedHtml += `<p>${paragraph}</p>`;
        }
    });
    
    return formattedHtml;
}

function appendMessage(message, isUser = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user-message' : 'ai-message'}`;
    
    const responseDiv = document.createElement('div');
    responseDiv.className = 'response-text';
    
    if (isUser) {
        responseDiv.innerHTML = `<p>${message}</p>`;
    } else {
        responseDiv.innerHTML = formatResponse(message);
    }
    
    messageDiv.appendChild(responseDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Event listener for the chat form
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const userInput = document.getElementById('userInput').value.trim();
            
            if (!userInput) return;
            
            // Display user message
            appendMessage(userInput, true);
            document.getElementById('userInput').value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userInput })
                });
                
                const data = await response.json();
                
                // Display AI response
                appendMessage(data.response);
                
            } catch (error) {
                console.error('Error:', error);
                appendMessage('عذراً، حدث خطأ في معالجة طلبك. الرجاء المحاولة مرة أخرى.');
            }
        });
    }
});

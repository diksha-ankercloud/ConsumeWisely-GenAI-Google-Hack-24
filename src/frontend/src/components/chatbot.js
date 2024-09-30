import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { FaCommentDots } from "react-icons/fa";


import { usellmResponse } from "../context/llmResponse";

function Chatbot() {
  const [show, setShow] = useState(false);
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { setLlmResponse } = usellmResponse();


  const handleClose = () => setShow(false);
  const handleShow = () => setShow(!show);
  function injectDataByClass(className, data) {
    // Wait for the DOM to be fully loaded
    document.addEventListener("DOMContentLoaded", function() {
      // Get the first element with the specified class name
      let element = document.getElementsByClassName(className)[0];
      
      // Check if the element exists
      if (element) {
        // Inject data into the element (text, value, or inner HTML)
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
          element.value = data;  // For input or textarea fields
        } else {
          element.innerHTML = data;  // For other elements like div, span, etc.
        }
      } else {
        console.log(`Element with class '${className}' not found.`);
      }
    });
  }
  
  // Example usage: Inject 'Hello World!' into the first element with the class 'my-class'
  function segregateMessage(data) {
    const message = data.message;
  
    // Segregating the fields using regex and string manipulation
    const result = {
      productName: message.match(/Product Name: ([^\n]+)/)?.[1]?.trim() || '',
      consumption: message.match(/Consumption: ([^\n]+)/)?.[1]?.trim() || '',
      category: message.match(/Category: ([^\n]+)/)?.[1]?.trim() || '',
      allergies: message.match(/Allergies: ([^\n]+)/)?.[1]?.trim() || '',
      dietType: message.match(/Diet Type: ([^\n]+)/)?.[1]?.trim() || '',
      similarProducts: message.match(/Similar Products: ([^\n]+)/)?.[1]?.trim() || '',
      caution: message.match(/Caution: ([^\n]+)/)?.[1]?.trim() || '',
    };
  
    return result;
  }

  const handleSendMessage = () => {
    if (message.trim() || selectedImage) {
      if (message.trim()) {
        setChatHistory((prev) => [...prev, { text: message, user: "You" }]);
      }
      if (imagePreview) {
        setChatHistory((prev) => [
          ...prev,
          { text: "", user: "You", image: imagePreview },
        ]);
      }

      sendToLLM(message, selectedImage);

      setMessage("");
      setSelectedImage(null);
      setImagePreview("");
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  function sendToLLM(msg, fileInput) {
    const formData = new FormData();
    formData.append("message", msg);

    if (fileInput) {
      formData.append("image", fileInput);
    }

    setIsLoading(true); // Set loading state

    fetch(`${process.env.REACT_APP_API_ENDPOINT}/get_response`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setChatHistory((prev) => [
          ...prev,
          { text: data.message, user: "Bot" },
        ]);
        setLlmResponse(segregateMessage(data))
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error during image upload:", error);
        setIsLoading(false);
      });
  }

  return (
    <>
      <div className="chatbot-icon" onClick={handleShow}>
        <FaCommentDots size={40} color="white" />
      </div>

      {show && (
        <div className="chatbot-modal">
          <div className="chat-window">
            <div className="chat-header">
              <h5>Chat with Us!</h5>
              <button className="close" onClick={handleClose}>
                &times;
              </button>
            </div>

            <div className="chat-body">
              {chatHistory.length === 0 && (
                <p className="text-muted">No messages yet.</p>
              )}
              {chatHistory.map((msg, index) => (
                <div
                  key={index}
                  className={`chat-message ${
                    msg.user === "You" ? "user-message" : "bot-message"
                  }`}
                >
                  <strong>{msg.user}:</strong>
                  <span>{msg.text}</span>
                  {msg.image && (
                    <div className="image-preview">
                      <img
                        src={msg.image}
                        alt="Uploaded"
                        style={{ maxWidth: "100px", marginTop: "10px" }}
                      />
                    </div>
                  )}
                </div>
              ))}
              {isLoading && <div className="loading">...</div>}{" "}
              {/* Three dots loading animation */}
            </div>

            <div className="chat-footer">
              <input
                type="text"
                className="form-control"
                placeholder="Type your message..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              />
              <button className="btn btn-warning" onClick={handleSendMessage}>
                Send
              </button>

              <input
                type="file"
                className="form-control"
                accept="image/*"
                onChange={handleImageChange}
                style={{ marginTop: "10px" }}
              />

              {imagePreview && (
                <div className="image-preview">
                  <p>Image Preview:</p>
                  <img
                    src={imagePreview}
                    alt="Selected"
                    style={{ maxWidth: "100px", marginTop: "10px" }}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .chatbot-icon {
          position: fixed;
          bottom: 20px;
          right: 20px;
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background-color: #ffc107;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
          z-index: 10000;
        }

        .chatbot-icon:hover {
          background-color: #ffc107;
        }

        .chatbot-modal {
          position: fixed;
          bottom: 90px;
          right: 20px;
          width: 400px;
        }

        .chat-window {
          background-color: white;
          border: 1px solid #ccc;
          border-radius: 10px;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
          display: flex;
          flex-direction: column;
          height: 650px;
          overflow: hidden;
        }

        .chat-header {
          background-color: #ffc107;
          color: white;
          padding: 10px;
          border-top-left-radius: 10px;
          border-top-right-radius: 10px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          z-index: 10000;
        }

        .chat-body {
          flex-grow: 1;
          padding: 10px;
          overflow-y: auto;
          background-color: #f9f9f9;
          z-index: 10000;
        }

        .chat-footer {
          display: flex;
          flex-direction: column;
          padding: 10px;
          border-top: 1px solid #ccc;
          z-index: 10000;
        }

        .chat-footer input[type="file"] {
          margin-top: 10px;
        }

        .chat-footer input[type="text"] {
          margin-bottom: 10px;
        }

        .chat-message {
          margin-bottom: 10px;
          display: flex;
          flex-direction: column;
        }

        .user-message {
          align-self: flex-end;
          text-align: right;
        }

        .bot-message {
          align-self: flex-start;
          text-align: left;
        }

        .loading {
          display: flex;
          justify-content: center;
          align-items: center;
          margin: 10px 0;
          font-size: 20px; /* Adjust size as needed */
        }

        .image-preview {
          align-self: flex-end; /* Align image preview to the right */
          margin-top: 10px;
        }

        .image-preview img {
          max-width: 100px;
        }
      `}</style>
    </>
  );
}

export default Chatbot;

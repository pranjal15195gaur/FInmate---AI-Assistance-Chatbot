'use client';
import React, { useState, useMemo } from 'react';
import PropTypes from 'prop-types';
import {
  CONVERSATION_END,
  HELP_START_OPTIONS,
  createNewAssistantMessage,
  createNewUserMessage,
  firstMessage,
  resetMessageIdCounter,
  getAIBotResponse,
} from '@/utils';
import ChatContext from './ChatContext';

export default function ChatProvider({ children }) {
  const [historicMessages, setHistoricMessages] = useState([]);
  const [messages, setMessages] = useState([firstMessage]);
  const [user, setUser] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isFinishedConversation, setIsFinishedConversation] = useState(false);
  const [requiredParams, setRequiredParams] = useState([]);
  const [currentParamIndex, setCurrentParamIndex] = useState(0);
  const [pendingParams, setPendingParams] = useState([]);
  const [currentQuery, setCurrentQuery] = useState('');

  const handleAssistantResponse = (response) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      createNewAssistantMessage(response.content, response.options, response.reference),
    ]);
  };

  const handleFallbackAssistantResponse = () => {
    if (!user) {
      setMessages((prevMessages) => [
        ...prevMessages, createNewAssistantMessage(null, HELP_START_OPTIONS),
      ]);
    } else {
      setMessages((prevMessages) => [...prevMessages, createNewAssistantMessage(null, [{
        id: 1, option: 'Loan', response: 'loan', description: 'Loan',
      }])]);
    }
  };

  const getBotResponse = async (message) => {
    console.log('User message:', message);
    setIsTyping(true);

    setTimeout(async () => {
      const lastMessage = messages[messages.length - 1].content;

      if (lastMessage.includes('username')) {
        setUser(message);
      }

      try {
        const aiResponse = await getAIBotResponse(message);

        if (aiResponse) {
          console.log('AI response:', aiResponse);
          handleAssistantResponse(aiResponse);

          // Handle missing parameters case
          if (aiResponse.content === 'Please provide the required parameters.') {
            console.log('Missing required parameters:', aiResponse.required_params);
            setRequiredParams(aiResponse.required_params);
            setCurrentParamIndex(0);
            setPendingParams([]);
            setCurrentQuery(message);
            // Ask for the first parameter immediately
            if (aiResponse.required_params.length > 0) {
              askNextParameter(aiResponse.required_params[0]);
            }
          }
        } else {
          handleFallbackAssistantResponse();
        }
      } catch (error) {
        console.error('Error fetching AI response:', error);
        handleFallbackAssistantResponse();
      }

      setIsTyping(false);
    }, 1000);
  };

  const askNextParameter = (param) => {
    setMessages((prevMessages) => [...prevMessages, createNewAssistantMessage(`Please provide ${param}:`)]);
  };

  const collectUserResponse = (response) => {
    console.log('User response:', response);
    console.log('Current param index:', currentParamIndex);
    if (currentParamIndex > requiredParams.length - 1) {
      var lastMessage = messages[messages.length - 1].content;
      console.log(lastMessage);
      if (lastMessage !== response.content){
        setMessages((prevMessages) => [...prevMessages, createNewUserMessage(response)]);
      }
    }
    
    setPendingParams((prevPendingParams) => {
      const updatedParams = [...prevPendingParams, response];
      const nextIndex = currentParamIndex + 1;
      
      if (nextIndex < requiredParams.length) {
        setCurrentParamIndex(nextIndex);
        askNextParameter(requiredParams[nextIndex]);
      } else {
        // All parameters collected, make API call
        const payload = updatedParams.reduce((acc, param, idx) => ({ ...acc, [requiredParams[idx]]: param }), {});
        console.log('payload', payload);
        var newPayload = convertPayload(payload);
        makeApiCall(newPayload);
      }
      
      return updatedParams;
    });
    
  };

  function convertPayload(payload) {
    const convertedPayload = {};
  
    for (const key in payload) {
      if (payload.hasOwnProperty(key)) {
        const value = payload[key];
        // Check if the value is a string and can be converted to an integer
        if (typeof value === 'string' && !isNaN(value) && Number.isInteger(parseFloat(value))) {
          convertedPayload[key] = parseInt(value, 10);
        } else {
          convertedPayload[key] = value;
        }
      }
    }
  
    return convertedPayload;
  }

  

  const makeApiCall = async (payload) => {
    // Add query to payload
    payload.query = currentQuery;

    try {
      const response = await fetch('http://localhost:5002/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('API response:', data);
      if (data.status === true) {
        handleAssistantResponse({ content: data.message });
      }
      else{
        handleAssistantResponse({ content: data.message });
      }

      // Reset states to revert to normal bot behavior
      setRequiredParams([]);
      setCurrentParamIndex(0);
      setPendingParams([]);
      setCurrentQuery('');

    } catch (error) {
      console.error('API error:', error);
      handleFallbackAssistantResponse();
    }
  };

  const finishConversation = () => {
    setIsFinishedConversation(true);
    setMessages((prevMessages) => [...prevMessages, createNewAssistantMessage('Bye! 👋')]);
    setHistoricMessages((prevMessages) => [...prevMessages, {
      id: prevMessages.length + 1,
      title: `Conversation ${user || 'user'} #${prevMessages.length + 1} - ${new Date().toLocaleString()}`,
      messages,
    }]);
    setUser('');
    setTimeout(() => {
      resetMessageIdCounter();
      setMessages([firstMessage]);
      setIsFinishedConversation(false);
    }, 2000);
  };

  const sendMessage = (message) => {
    const lastMessage = messages[messages.length - 1].content;

    if (!lastMessage.includes('password')) {
      setMessages((prevMessages) => [...prevMessages, createNewUserMessage(message)]);
    }

    if (message === CONVERSATION_END) {
      finishConversation();
    } else {
      if (requiredParams.length > 0 && currentParamIndex < requiredParams.length) {
        collectUserResponse(message);
      } else {
        getBotResponse(message);
      }
    }
  };

  const contextType = useMemo(
    () => (
      {
        messages, sendMessage, historicMessages, isTyping, isFinishedConversation,
      }),
    [messages, sendMessage, historicMessages, isTyping, isFinishedConversation],
  );

  return (
    <ChatContext.Provider value={contextType}>
      {children}
    </ChatContext.Provider>
  );
}

ChatProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

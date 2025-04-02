// 설정 페이지 관련 JavaScript

// 기본 설정값
const defaultSettings = {
    llm: {
        provider: 'local',
        model: 'custom-model',
        apiKey: '',
        serverIp: "127.0.0.1",
        serverPort: "11434"
    },
    tts: {
        provider: 'edge',
        voice: 'en-IE-EmilyNeural',
        speed: 110
    },
    system: {
        prompt: "You are named Aki. Pretend you're my cute anime assistant. Please respond simple and politely. Do NOT USE INTERJECTION!",
        language: 'en'
    }
};

// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    // 설정 모달 요소
    //const settingsContainer = document.getElementById('settings-container'); // Remove this line
    
    // 닫기 버튼
    const closeSettings = document.getElementById('close-settings');
    
    // 저장, 취소, 초기화 버튼
    const saveSettingsBtn = document.getElementById('save-settings');
    const cancelSettingsBtn = document.getElementById('cancel-settings');
    const resetDefaultsBtn = document.getElementById('reset-defaults');
    
    // 테스트 음성 버튼
    const testVoiceBtn = document.getElementById('test-voice');
    
    // 채팅 기록 삭제 버튼
    const clearHistoryBtn = document.getElementById('clear-history');
    
    // LLM Provider 선택 요소
    const llmProviderSelect = document.getElementById('llm-provider');
    
    // 로컬 서버 설정 섹션
    const localServerSettings = document.getElementById('local-server-settings');
    
    // 음성 속도 슬라이더
    const voiceSpeedSlider = document.getElementById('voice-speed');
    const voiceSpeedValue = document.querySelector('.slider-value');
    
    // 설정 모달 닫기
    // function closeSettingsModal() { // Remove this function
    //     // 부모 창에 취소 메시지 전송
    //     //window.parent.postMessage({ action: 'cancelSettings' }, '*');
    //     //settingsContainer.style.display = 'none';
    // }

    fetch('/get_settings')
        .then(response => response.json())
        .then(data => {
            console.log("Settings data:", data); // Check if data is received correctly
            // Update the UI with the received settings
            const llmProvider = document.getElementById('llm-provider');
            const llmModel = document.getElementById('llm-model');
            const llmApiKey = document.getElementById('api-key');
            const llmServerIp = document.getElementById('server-ip');
            const llmServerPort = document.getElementById('server-port');
            const ttsProvider = document.getElementById('tts-provider');
            const ttsVoice = document.getElementById('tts-voice');
            const voiceSpeed = document.getElementById('voice-speed');
            const systemPrompt = document.getElementById('system-prompt');
            const language = document.getElementById('language');

            if (llmProvider) llmProvider.value = data.llm.provider;
            if (llmModel) llmModel.value = data.llm.model;
            if (llmApiKey) llmApiKey.value = data.llm.apiKey;
            if (llmServerIp) llmServerIp.value = data.llm.serverIp;
            if (llmServerPort) llmServerPort.value = data.llm.serverPort;
            if (ttsProvider) ttsProvider.value = data.tts.provider;
            if (ttsVoice) ttsVoice.value = data.tts.voice;
            if (voiceSpeed) voiceSpeed.value = data.tts.speed;
            if (systemPrompt) systemPrompt.value = data.system.prompt;
            if (language) language.value = data.system.language;
        })
        .catch(error => console.error('Error fetching settings:', error));

    // 설정 저장하기
    function saveSettings(event) {
        event.preventDefault(); // Prevent page reload
        // 설정 값 가져오기
        const settings = {
            llm: {
                //provider: llmProviderSelect.value,
                provider: document.getElementById('llm-provider').value,
                model: document.getElementById('llm-model').value,
                apiKey: document.getElementById('api-key').value,
                serverIp: document.getElementById('server-ip').value,
                serverPort: document.getElementById('server-port').value
            },
            tts: {
                provider: document.getElementById('tts-provider').value,
                voice: document.getElementById('tts-voice').value,
                speed: parseInt(voiceSpeedSlider.value)
            },
            system: {
                prompt: document.getElementById('system-prompt').value,
                language: document.getElementById('language').value
            }
        };
        
        // 백엔드에 설정 전송 (필요한 경우)
        fetch('/update_settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settings),
        })
        .then(response => response.json())
        .then(data => {
            console.log('설정이 백엔드에 적용되었습니다:', data);
            showNotification('설정이 저장되었습니다.');
            //closeSettingsModal(); // Remove this line
            window.parent.postMessage({ action: 'closeSettingsModal' }, '*');
        })
        .catch(error => {
            console.error('백엔드에 설정을 적용하는 중 오류가 발생했습니다:', error);
            showNotification('설정 저장에 실패했습니다.', true);
        });
    }
    
    // 기본값으로 초기화
    function resetToDefaults() {
        if (confirm('모든 설정을 기본값으로 초기화하시겠습니까?')) {
            const settings = defaultSettings;
            
            // 백엔드에 설정 전송 (필요한 경우)
            fetch('/update_settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings),
            })
            .then(response => response.json())
            .then(data => {
                console.log('설정이 백엔드에 적용되었습니다:', data);
                showNotification('설정이 기본값으로 초기화되었습니다.');
            })
            .catch(error => {
                console.error('백엔드에 설정을 적용하는 중 오류가 발생했습니다:', error);
                showNotification('설정 저장에 실패했습니다.', true);
            });
            
            // 기본 설정 값
            llmProviderSelect.value = 'local';
            document.getElementById('llm-model').value = 'gemma3:latest';
            document.getElementById('api-key').value = '';
            document.getElementById('tts-provider').value = 'edge';
            document.getElementById('tts-voice').value = 'ko-KR-SunHiNeural';
            voiceSpeedSlider.value = 110;
            updateVoiceSpeedValue();
            document.getElementById('system-prompt').value = 'You are named Aki. Pretend you\'re my cute anime assistant. Please respond simple and politely. Do NOT USE INTERJECTION!';
            document.getElementById('language').value = 'en';
            document.getElementById('server-ip').value = '127.0.0.1';
            document.getElementById('server-port').value = '11434';
            
            // LLM Provider에 따라 로컬 서버 설정 표시/숨김
            toggleLocalServerSettings();
        }
    }
    
    // 음성 속도 값 업데이트
    function updateVoiceSpeedValue() {
        const value = voiceSpeedSlider.value;
        const percentage = Math.round((value - 100) / 10) * 10;
        
        if (percentage > 0) {
            voiceSpeedValue.textContent = `+${percentage}%`;
        } else if (percentage < 0) {
            voiceSpeedValue.textContent = `${percentage}%`;
        } else {
            voiceSpeedValue.textContent = `0%`;
        }
    }
    
    // 테스트 음성 재생
    function testVoice() {
        const settings = {
            tts: {
                provider: document.getElementById('tts-provider').value,
                voice: document.getElementById('tts-voice').value,
                speed: parseInt(voiceSpeedSlider.value)
            }
        };
        const testText = "안녕하세요, 음성 테스트입니다.";
        
        fetch('/test_voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: testText,
                provider: settings.tts.provider,
                voice: settings.tts.voice,
                speed: settings.tts.speed
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.audio_url) {
                const audio = new Audio(data.audio_url);
                audio.play();
            } else {
                showNotification('음성 테스트에 실패했습니다.', true);
            }
        })
        .catch(error => {
            console.error('음성 테스트 중 오류가 발생했습니다:', error);
            showNotification('음성 테스트에 실패했습니다.', true);
        });
    }
    
    // 채팅 기록 삭제
    function clearChatHistory() {
        if (confirm('모든 채팅 기록을 삭제하시겠습니까?')) {
            fetch('/clear_history', {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('대화 기록이 삭제되었습니다.');
                    // 채팅 UI 초기화
                    //document.querySelector('.message-list').innerHTML = '';
                } else {
                    showNotification('대화 기록 삭제에 실패했습니다.', true);
                }
            })
            .catch(error => {
                console.error('대화 기록 삭제 중 오류가 발생했습니다:', error);
                showNotification('대화 기록 삭제에 실패했습니다.', true);
            });
        }
    }
    
    // LLM Provider에 따라 로컬 서버 설정 표시/숨김
    function toggleLocalServerSettings() {
        if (llmProviderSelect.value === 'local') {
            localServerSettings.style.display = 'block';
        } else {
            localServerSettings.style.display = 'none';
        }
    }

    // llmProviderSelect = document.getElementById('llm-provider');
    
    if (llmProviderSelect.value === 'local') {
        // LLM Model 가져오기
        function fetchOllamaModels() {
            const serverIp = document.getElementById('server-ip').value;
            const serverPort = document.getElementById('server-port').value;
        
            fetch('/get_ollama_models', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ serverIp: serverIp, serverPort: serverPort })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const llmModelSelect = document.getElementById('llm-model');
                    llmModelSelect.innerHTML = ''; // Clear existing options
        
                    data.models.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model;
                        option.text = model;
                        llmModelSelect.appendChild(option);
                    });
                } else {
                    showNotification('Ollama 모델 목록을 가져오는데 실패했습니다.', true);
                }
            })
            .catch(error => {
                console.error('Error fetching Ollama models:', error);
                showNotification('Ollama 모델 목록을 가져오는데 실패했습니다.', true);
            });
        }
    }

    // 이벤트 리스너 등록
    closeSettings.addEventListener('click', function() {
        window.parent.postMessage({ action: 'closeSettingsModal' }, '*');
    });
    //saveSettingsBtn.addEventListener('click', saveSettings);
    saveSettingsBtn.addEventListener('click', function(event) {
        saveSettings(event);
    });
    cancelSettingsBtn.addEventListener('click', function() {
        window.parent.postMessage({ action: 'closeSettingsModal' }, '*');
    });
    resetDefaultsBtn.addEventListener('click', resetToDefaults);
    testVoiceBtn.addEventListener('click', testVoice);
    clearHistoryBtn.addEventListener('click', clearChatHistory);
    
    // 음성 속도 슬라이더 이벤트
    voiceSpeedSlider.addEventListener('input', updateVoiceSpeedValue);
    
    // Listen for the loadSettings message from the parent window
    window.addEventListener('message', function(event) {
        if (event.data.action === 'loadSettings') {
            const settings = event.data.settings;
            console.log("Received settings:", settings);
            // Apply the settings to the form
            document.getElementById('llm-provider').value = settings.llm.provider; // Corrected line
            document.getElementById('llm-model').value = settings.llm.model; // Corrected line
            document.getElementById('api-key').value = settings.llm.apiKey; // Corrected line
            document.getElementById('server-ip').value = settings.llm.serverIp; 
            document.getElementById('server-port').value = settings.llm.serverPort; 
            document.getElementById('tts-provider').value = settings.tts.provider; // Corrected line
            document.getElementById('tts-voice').value = settings.tts.voice; // Corrected line
            document.getElementById('voice-speed').value = settings.tts.speed; // Corrected line
            updateVoiceSpeedValue(); // Corrected line
            document.getElementById('system-prompt').value = settings.system.prompt; // Corrected line
            document.getElementById('language').value = settings.system.language; // Corrected line
            
            // Select the correct model
            const currentProvider = document.getElementById('llm-provider').value;
            const currentModel = settings.llm.model;
            
            // Find the correct model
            const correctModel = document.getElementById('llm-model').querySelector(`option[value="${currentModel}"]`);
            if (correctModel) {
                correctModel.selected = true;
            }
            
            // LLM Provider에 따라 로컬 서버 설정 표시/숨김
            toggleLocalServerSettings();

            // Fetch Ollama models if the provider is local
            // if (currentProvider === 'local') {
            //      fetchOllamaModels(); // Add this line
            // }

            // LLM Provider 변경 이벤트
            if (llmProviderSelect) {
                llmProviderSelect.addEventListener('change', function() { 
                    // LLM Provider에 따라 모델 옵션 변경
                    const llmModelSelect = document.getElementById('llm-model');
                    llmModelSelect.innerHTML = '';
                    
                    let options = [];
                    
                    switch (this.value) {
                        case 'anthropic':
                            options = [
                                { value: 'claude-3-7-sonnet-latest', text: 'Claude 3.7 Sonnet' },
                                { value: 'claude-3-7-haiku-latest', text: 'Claude 3.7 Haiku' }
                            ];
                            break;
                        case 'chatgpt':
                            options = [
                                { value: 'gpt-4o', text: 'GPT-4o' },
                                { value: 'o1', text: 'GPT-o1' },
                                { value: 'o3-mini', text: 'GPT-o3 mini' }
                            ];
                            break;
                        case 'deepseek':
                                options = [
                                    { value: 'deepseek-chat', text: 'DeepSeek Chat' }
                                ];
                                break;
                        case 'gemini':
                            options = [
                                { value: 'gemini-2.5-pro-exp-03-25', text: 'Gemini 2.5 Pro' },
                                { value: 'gemini-2.0-flash', text: 'Gemini 2.0 Flash' },
                                { value: 'gemini-2.0-flash-lite', text: 'Gemini 2.0 Flash-Lite' }
                            ];
                            break;
                        case 'local':
                            // options = [
                            //     { value: 'custom-model', text: '사용자 정의 모델' }
                            // ];
                            fetchOllamaModels();
                            break;
                        default:
                            options = [
                                { value: 'default-model', text: '기본 모델' }
                            ];
                    }
                    
                    // 새 옵션 추가
                    options.forEach(option => {
                        const optionElement = document.createElement('option');
                        optionElement.value = option.value;
                        optionElement.textContent = option.text;
                        llmModelSelect.appendChild(optionElement);
                    });
                    
                    // 첫 번째 옵션 선택
                    if (options.length > 0) {
                        llmModelSelect.value = options[0].value;
                    }
                    
                    // 로컬 서버 설정 표시/숨김
                    toggleLocalServerSettings();
                    
                    // Select the correct model
                    const currentProvider = document.getElementById('llm-provider').value;
                    const currentModel = document.getElementById('llm-model').value;
                    
                    // Find the correct model
                    const correctModel = document.getElementById('llm-model').querySelector(`option[value="${currentModel}"]`);
                    if (correctModel) {
                        correctModel.selected = true;
                    }
                }); // Add this line
            } // Add this line
        }
    });

    // LLM Model 드롭다운 메뉴 클릭 시
    // const llmModelSelect = document.getElementById('llm-model');
    // if (llmModelSelect) {
    //     llmModelSelect.addEventListener('click', function() {
    //         // LLM Provider가 "Local Server"일 때만 모델 목록 업데이트
    //         if (llmProviderSelect.value === 'local') {
    //             fetchOllamaModels();
    //         }
    //     });
    // }
});

// 알림 표시
function showNotification(message, isError = false) {
    const notification = document.createElement('div');
    notification.className = `notification ${isError ? 'error' : 'success'}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // 애니메이션 효과
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // 3초 후 제거
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 알림 스타일 추가
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
.notification {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px 20px;
    border-radius: 5px;
    color: white;
    font-size: 14px;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s, transform 0.3s;
    z-index: 2000;
}

.notification.success {
    background-color: #28a745;
}

.notification.error {
    background-color: #dc3545;
}

.notification.show {
    opacity: 1;
    transform: translateY(0);
}
`;
document.head.appendChild(notificationStyle);

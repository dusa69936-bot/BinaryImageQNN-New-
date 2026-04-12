import React, { useRef, useState, useEffect } from 'react';
import { StyleSheet, SafeAreaView, StatusBar, BackHandler, ActivityIndicator, View, Alert, Text, Vibration } from 'react-native';
import { WebView } from 'react-native-webview';
import * as Speech from 'expo-speech'; // 🔥 The Secret Sauce for Voice

export default function App() {
  const webViewRef = useRef(null);
  const canGoBackRef = useRef(false);
  const [debugText, setDebugText] = useState("Voi-Bridge Ready");
  const [lastMessage, setLastMessage] = useState("");

  // 🔥 Your live Production URL (Adding version to bust cache)
  const targetUrl = 'https://binaryimageqnn-1.onrender.com?v=' + Date.now();

  // Handle Android back button
  React.useEffect(() => {
    const handleBackButton = () => {
      if (canGoBackRef.current && webViewRef.current) {
        webViewRef.current.goBack();
        return true;
      }
      return false; // let default behavior happen (exit app)
    };

    BackHandler.addEventListener('hardwareBackPress', handleBackButton);
    return () => {
      BackHandler.removeEventListener('hardwareBackPress', handleBackButton);
    };
  }, []);

  // 🔥 Initial Test to see if phone speaker is working
  useEffect(() => {
    setTimeout(() => {
      setDebugText("Testing Speaker...");
      Speech.speak("System Online", { 
        rate: 0.9,
        onStart: () => setDebugText("Speaker Working!"),
        onError: (e) => Alert.alert("Speaker Error", "Voice engine failed: " + e.message)
      });
    }, 3000);
  }, []);

  // 🔥 Speech Bridge Logic to bypass WebView restrictions
  const handleMessage = (event) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.type === 'SPEAK' && data.text) {
        setDebugText("Request Received...");
        setLastMessage(data.text);
        Vibration.vibrate(100); 
        
        Speech.speak(data.text, {
          language: data.lang || 'en-US',
          pitch: 1.0,
          rate: 0.9,
          onStart: () => setDebugText("Speaking Now"),
          onDone: () => setDebugText("Finished Speaking"),
          onError: (e) => {
            setDebugText("Voice Fail!");
            Alert.alert("Speech Error", "Could not play: " + data.text + "\nReason: " + e.message);
          }
        });
      }
    } catch (e) {
      console.log("WebView Message Error:", e);
    }
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#020617" />
      
      <WebView
        ref={webViewRef}
        source={{ uri: targetUrl }}
        style={styles.webview}
        originWhitelist={['*']}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        sharedCookiesEnabled={true}
        thirdPartyCookiesEnabled={true}
        userAgent="ReactNative-Bridge-Quantum" 
        injectedJavaScript={`window.isReactNativeWebView = true; true;`}
        setSupportMultipleWindows={false}
        mediaPlaybackRequiresUserAction={false} 
        allowsInlineMediaPlayback={true}        
        allowsFullscreenVideo={true}
        allowFileAccess={true}
        scalesPageToFit={true}
        mixedContentMode="always"
        onMessage={handleMessage}
        onShouldStartLoadWithRequest={(request) => {
          // 🔥 Block Google TTS & external audio URLs from navigating
          const blocked = ['translate.google.com', 'translate_tts', 'gstatic.com'];
          const isBlocked = blocked.some(b => request.url.includes(b));
          if (isBlocked) return false; // Block navigation, don't follow
          return true; // Allow everything else
        }}
        onNavigationStateChange={(navState) => {
          canGoBackRef.current = navState.canGoBack;
        }}
      />

      {/* 🔥 DEBUG OVERLAY with RELOAD */}
      <View style={{ 
          position: 'absolute', bottom: 20, left: 20, right: 20, 
          backgroundColor: 'rgba(2, 6, 23, 0.95)', padding: 15, borderRadius: 20,
          borderWidth: 1, borderColor: '#4ade80', flexDirection: 'row', alignItems: 'center'
      }}>
        <View style={{ flex: 1 }}>
          <Text style={{ color: '#4ade80', fontWeight: 'bold', fontSize: 12 }}>System: {debugText}</Text>
          <Text style={{ color: 'white', marginTop: 5, fontSize: 10 }}>Last: {lastMessage || "None"}</Text>
        </View>
        <Text 
          onPress={() => webViewRef.current?.reload()}
          style={{ backgroundColor: '#4ade80', color: 'black', padding: 8, borderRadius: 10, fontSize: 10, fontWeight: 'bold' }}>
          RELOAD
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  webview: {
    flex: 1,
  },
  loaderContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ffffff',
  },
});

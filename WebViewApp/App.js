import React, { useRef, useState, useEffect } from 'react';
import { StyleSheet, SafeAreaView, StatusBar, BackHandler, ActivityIndicator, View, Alert, Text, Vibration } from 'react-native';
import { WebView } from 'react-native-webview';
import * as Speech from 'expo-speech'; // 🔥 The Secret Sauce for Voice

export default function App() {
  const webViewRef = useRef(null);
  const canGoBackRef = useRef(false);
  const [debugText, setDebugText] = useState("Voi-Bridge Ready");
  const [lastMessage, setLastMessage] = useState("");

  // 🔥 Your live Production URL
  const targetUrl = 'https://binaryimageqnn-1.onrender.com';

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
  React.useEffect(() => {
    setTimeout(() => {
      Speech.speak("Quantum Bridge Active", { rate: 0.9 });
    }, 2000);
  }, []);

  // 🔥 Speech Bridge Logic to bypass WebView restrictions
  const handleMessage = (event) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.type === 'SPEAK' && data.text) {
        setDebugText("Speaking...");
        setLastMessage(data.text);
        Vibration.vibrate(100); // 📳 Shake phone on voice request
        
        Speech.stop();
        Speech.speak(data.text, {
          language: data.lang || 'en-US',
          pitch: 1.0,
          rate: 0.9,
          onDone: () => setDebugText("Voice Done"),
          onError: () => setDebugText("Voice Error!")
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
        setSupportMultipleWindows={false}
        mediaPlaybackRequiresUserAction={false} 
        allowsInlineMediaPlayback={true}        
        allowsFullscreenVideo={true}
        allowFileAccess={true}
        scalesPageToFit={true}
        mixedContentMode="always"
        onMessage={handleMessage} 
        onNavigationStateChange={(navState) => {
          canGoBackRef.current = navState.canGoBack;
        }}
      />

      {/* 🔥 DEBUG OVERLAY: మీకు మొబైల్ లో కనిపించడం కోసం */}
      <View style={{ 
          position: 'absolute', bottom: 20, left: 20, right: 20, 
          backgroundColor: 'rgba(0,0,0,0.8)', padding: 15, borderRadius: 20,
          borderWidth: 1, borderColor: '#4ade80', pointerEvents: 'none'
      }}>
        <Text style={{ color: '#4ade80', fontWeight: 'bold', fontSize: 12 }}>System: {debugText}</Text>
        <Text style={{ color: 'white', marginTop: 5, fontSize: 10 }}>Last: {lastMessage || "None"}</Text>
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

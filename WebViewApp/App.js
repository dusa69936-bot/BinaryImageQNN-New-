import React, { useRef, useState, useEffect } from 'react';
import { StyleSheet, BackHandler, StatusBar, View, Alert, Text, Vibration } from 'react-native';
import { WebView } from 'react-native-webview';
import * as Speech from 'expo-speech';

export default function App() {
  const webViewRef = useRef(null);
  const canGoBackRef = useRef(false);
  const [debugText, setDebugText] = useState("System Ready");
  const [lastMessage, setLastMessage] = useState("");

  const targetUrl = 'https://binaryimageqnn-1.onrender.com?v=' + Date.now();

  useEffect(() => {
    const subscription = BackHandler.addEventListener('hardwareBackPress', () => {
      if (canGoBackRef.current && webViewRef.current) {
        webViewRef.current.goBack();
        return true;
      }
      return false;
    });
    return () => subscription.remove();
  }, []);

  useEffect(() => {
    setTimeout(() => {
      Speech.speak("System Online", {
        rate: 0.9,
        onStart: () => setDebugText("Speaker OK"),
        onError: () => setDebugText("Speaker ERR")
      });
    }, 2000);
  }, []);

  const handleMessage = (event) => {
    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data.type === 'SPEAK' && data.text) {
        setDebugText("Speaking...");
        setLastMessage(data.text);
        Vibration.vibrate(80);
        Speech.speak(data.text, {
          language: data.lang || 'en-US',
          pitch: 1.0,
          rate: 0.9,
          onDone: () => setDebugText("Done ✓"),
          onError: () => setDebugText("Voice Err")
        });
      }
    } catch (e) {
      console.log("Bridge Error:", e);
    }
  };

  const shouldStartLoad = (request) => {
    const url = request.url;
    if (url.startsWith('https://binaryimageqnn-1.onrender.com') || url.startsWith('about:blank') || url.startsWith('data:')) {
      return true;
    }
    // Block unexpected redirects
    return false;
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
        onShouldStartLoadWithRequest={shouldStartLoad}
        onNavigationStateChange={(navState) => {
          canGoBackRef.current = navState.canGoBack;
        }}
      />
      
      {/* Mini Debug (Invisible to users, visible when knowing where to look) */}
      <View style={{ position: 'absolute', top: 50, right: 10, opacity: 0.5 }}>
          <Text style={{ color: '#4ade80', fontSize: 8 }}>{debugText}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#020617' },
  webview: { flex: 1, backgroundColor: '#020617' }
});

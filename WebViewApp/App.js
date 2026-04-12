import React, { useRef, useState, useEffect } from 'react';
import { StyleSheet, BackHandler, StatusBar, View, Alert, Text, Vibration } from 'react-native';
import { WebView } from 'react-native-webview';
import * as Speech from 'expo-speech';

export default function App() {
  const webViewRef = useRef(null);
  const canGoBackRef = useRef(false);
  const [debugText, setDebugText] = useState("Bridge Ready");
  const [lastMessage, setLastMessage] = useState("");

  const targetUrl = 'https://binaryimageqnn-1.onrender.com';

  // ✅ Fixed BackHandler (new subscription pattern)
  useEffect(() => {
    const subscription = BackHandler.addEventListener('hardwareBackPress', () => {
      if (canGoBackRef.current && webViewRef.current) {
        webViewRef.current.goBack();
        return true;
      }
      return false;
    });
    return () => subscription.remove(); // ✅ Correct cleanup
  }, []);

  // 🔥 Startup Voice Test
  useEffect(() => {
    setTimeout(() => {
      setDebugText("Testing Speaker...");
      Speech.speak("System Online", {
        rate: 0.9,
        onStart: () => setDebugText("Speaker Working!"),
        onError: () => setDebugText("Speaker Error!")
      });
    }, 3000);
  }, []);

  // 🔥 Bridge: Receive SPEAK messages from website
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
          onError: () => setDebugText("Voice Error!")
        });
      }
    } catch (e) {
      console.log("Bridge Error:", e);
    }
  };

  // 🔥 Block any URL that should NOT cause navigation
  const shouldStartLoad = (request) => {
    const url = request.url;
    // Allow only our main app URL
    if (url.startsWith('https://binaryimageqnn-1.onrender.com')) return true;
    if (url.startsWith('about:blank')) return true;
    if (url.startsWith('data:')) return true;
    // Block everything else (Google TTS, external links, etc.)
    console.log("Blocked navigation to:", url);
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

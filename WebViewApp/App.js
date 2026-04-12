import React, { useRef, useState } from 'react';
import { StyleSheet, SafeAreaView, StatusBar, BackHandler, ActivityIndicator, View } from 'react-native';
import { WebView } from 'react-native-webview';
import * as Speech from 'expo-speech'; // 🔥 The Secret Sauce for Voice

export default function App() {
  const webViewRef = useRef(null);
  const canGoBackRef = useRef(false);

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
        console.log("Speaking via Bridge:", data.text, data.lang);
        
        // We stop any ongoing speech to start the new one fresh
        Speech.stop();

        Speech.speak(data.text, {
          language: data.lang || 'en-US',
          pitch: 1.0,
          rate: 0.9,
          onStart: () => console.log("Speech started"),
          onDone: () => console.log("Speech finished"),
          onError: (e) => {
            console.log("Speech engine error:", e);
            // Fallback to English if original language fails
            Speech.speak(data.text, { language: 'en-US' });
          }
        });
      }
    } catch (e) {
      console.log("WebView Message Error:", e);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#ffffff" />
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
        mediaPlaybackRequiresUserAction={false} // 🔥 Important for Auto-Speech
        allowsInlineMediaPlayback={true}        // 🔥 Important for iOS
        allowsFullscreenVideo={true}
        allowFileAccess={true}
        scalesPageToFit={true}
        mixedContentMode="always"
        onMessage={handleMessage} // 🔥 Hook up the bridge
        onNavigationStateChange={(navState) => {
          canGoBackRef.current = navState.canGoBack;
        }}
      />
    </SafeAreaView>
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

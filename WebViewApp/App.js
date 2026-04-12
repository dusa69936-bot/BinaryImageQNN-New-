import React, { useRef, useState } from 'react';
import { StyleSheet, SafeAreaView, StatusBar, BackHandler, ActivityIndicator, View } from 'react-native';
import { WebView } from 'react-native-webview';

export default function App() {
  const webViewRef = useRef(null);
  const canGoBackRef = useRef(false);

  // 🔥 Your live Production URL
  const targetUrl = 'https://binary-image-qnn-new.onrender.com';

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
        mediaPlaybackRequiresUserAction={false} // 🔥 Allows speech/sound without restriction
        allowsInlineMediaPlayback={true}        // 🔥 For iOS support
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

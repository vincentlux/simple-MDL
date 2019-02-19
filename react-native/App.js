import React, { Component } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableHighlight,
  axios
} from 'react-native';
import { getResult } from './components/GetResult'


export default class SearchComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      error: false
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleChange(e) {
    this.setState({
      username: e.nativeEvent.text
    });
  }
  handleSubmit() {
    console.log(this.state.username);
    console.log("hi there")
    getResult(this.state.username)
      .then((responseJson) => { console.log(responseJson) })
      .catch((error) => { console.error(error); });
  }

  render() {
    return (
      <View style={styles.main}>
        <Text style={styles.title}>MDL Search</Text>
        <TextInput
              style={styles.searchInput}
              onChange={this.handleChange}
            />
        <TouchableHighlight
                style = {styles.button}
                underlayColor= "white"
                onPress={this.handleSubmit}
              >
              <Text
                  style={styles.buttonText}>
                  SEARCH
              </Text>
            </TouchableHighlight>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  main: {
    flex: 1,
    padding: 30,
    marginTop: 65,
    flexDirection: 'column',
    justifyContent: 'center',
    backgroundColor: '#2a8ab7'
  },
  title: {
    marginBottom: 20,
    fontSize: 25,
    textAlign: 'center'
  },
  searchInput: {
    height: 50,
    padding: 4,
    marginRight: 5,
    fontSize: 23,
    borderWidth: 1,
    borderColor: 'white',
    borderRadius: 8,
    color: 'white'
  },
  buttonText: {
    fontSize: 18,
    color: '#111',
    alignSelf: 'center'
  },
  button: {
    height: 45,
    flexDirection: 'row',
    backgroundColor:'white',
    borderColor: 'white',
    borderWidth: 1,
    borderRadius: 8,
    marginBottom: 10,
    marginTop: 10,
    alignSelf: 'stretch',
    justifyContent: 'center'
  }
});

// import React, { Component } from 'react';
// import { AppRegistry, StyleSheet, Text, View } from 'react-native';
// const styles = StyleSheet.create({
//   bigBlue: {
//     color: 'blue',
//     fontWeight: 'bold',
//     fontSize: 30,
//   },
//   red: {
//     color: 'red',
//   },
// });

// export default class LotsOfStyles extends Component {
//   render() {
//     return (
//       <View>
//         <Text style={styles.red}>just red</Text>
//         <Text style={styles.bigBlue}>just bigBlue</Text>
//         <Text style={[styles.bigBlue, styles.red]}>bigBlue, then red</Text>
//         <Text style={[styles.red, styles.bigBlue]}>red, then bigBlue</Text>
//       </View>
//     );
//   }
// }

// // skip this line if using Create React Native App
// AppRegistry.registerComponent('AwesomeProject', () => LotsOfStyles);
// // keep FOLLOW https://facebook.github.io/react-native/docs/props


// // import React from 'react';
// // import { Platform, StatusBar, StyleSheet, View } from 'react-native';
// // import { AppLoading, Asset, Font, Icon } from 'expo';
// // import AppNavigator from './navigation/AppNavigator';

// // export default class App extends React.Component {
// //   state = {
// //     isLoadingComplete: false,
// //   };

// //   render() {
// //     if (!this.state.isLoadingComplete && !this.props.skipLoadingScreen) {
// //       return (
// //         <AppLoading
// //           startAsync={this._loadResourcesAsync}
// //           onError={this._handleLoadingError}
// //           onFinish={this._handleFinishLoading}
// //         />
// //       );
// //     } else {
// //       return (
// //         <View style={styles.container}>
// //           {Platform.OS === 'ios' && <StatusBar barStyle="default" />}
// //           <AppNavigator />
// //         </View>
// //       );
// //     }
// //   }

// //   _loadResourcesAsync = async () => {
// //     return Promise.all([
// //       Asset.loadAsync([
// //         require('./assets/images/robot-dev.png'),
// //         require('./assets/images/robot-prod.png'),
// //       ]),
// //       Font.loadAsync({
// //         // This is the font that we are using for our tab bar
// //         ...Icon.Ionicons.font,
// //         // We include SpaceMono because we use it in HomeScreen.js. Feel free
// //         // to remove this if you are not using it in your app
// //         'space-mono': require('./assets/fonts/SpaceMono-Regular.ttf'),
// //       }),
// //     ]);
// //   };

// //   _handleLoadingError = error => {
// //     // In this case, you might want to report the error to your error
// //     // reporting service, for example Sentry
// //     console.warn(error);
// //   };

// //   _handleFinishLoading = () => {
// //     this.setState({ isLoadingComplete: true });
// //   };
// // }

// // const styles = StyleSheet.create({
// //   container: {
// //     flex: 1,
// //     backgroundColor: '#fff',
// //   },
// // });

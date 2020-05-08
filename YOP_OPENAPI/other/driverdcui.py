 package com.yongche.driver.tools;

import static com.jayway.jsonassert.JsonAssert.with;
import static org.hamcrest.Matchers.equalTo;
import static org.junit.Assert.assertEquals;

import java.util.HashMap;

import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import com.github.kevinsawicki.http.HttpRequest;
import com.jayway.jsonpath.JsonPath;
import com.yongche.driver.data.DriverInfo;

public class GetToken {
public static final RequestHeaderConfig header;
public static HttpRequest request;
public static String response;
public static String oauth_token_secret;
public static int code;
public static String oauth_token;
public static final DriverInfo driver;
public static final RequestUrlConfig url;

private static HashMap<String, String> prameters;

static {
header = new RequestHeaderConfig();
url = new RequestUrlConfig("/Driver/VerifyCooperaStatus");
driver = new DriverInfo().getOffLineDriverWithImei();
prameters = new HashMap<String, String>();
}

@BeforeClass
public static void setUp() {

// get verification code
prameters.put("vehicle_number", driver.vehicle_number);
prameters.put("is_gzip", "1");
prameters.put("cellphone", driver.cellPhone);
prameters.put("area_code", "86");
prameters.put("version", "93");
prameters.put("imei", driver.imei);
prameters.put("x_auth_mode", "client_auth");
response = new RequestMulitAssemble(url.getUrl(), prameters, header).getResponse_getMethod();
String password = JsonPath.read(response, "$.msg.password" + "\r\n").toString();

url.path = "/oauth/accessToken";
prameters.put("imei", driver.imei);
prameters.put("x_auth_username", driver.cellPhone);
prameters.put("x_auth_password", password);
System.out.println(response);

request = new RequestMulitAssemble(url.getUrl(), prameters, header).getHttpRequest_postMethod();
code = request.code();
response = request.body();

oauth_token = JsonPath.read(response, "$.msg.oauth_token" + "\r\n");
oauth_token_secret = JsonPath.read(response, "$.msg.oauth_token_secret" + "\r\n");

}

public static String GetAcessToken() {
if (oauth_token == null) {
GetToken.setUp();
return oauth_token;
}
return oauth_token;
}

// public static String getToken_Secret() {
// if (oauth_token_secret == null) {
// GetToken.setUp();
// return oauth_token_secret;
// }
// return oauth_token_secret;
// }

@Test
public void testResponseCodeSuccess() {
assertEquals(200, code);
}

@Test
public void testResponseWithSuccessCode() {
with(response).assertThat("$.code", equalTo(200));
}

@Test
public void testOauth_tokenNotNull() {
with(response).assertNotNull("$.msg.oauth_token");
}

@Test
public void testOauth_token_secretNotNull() {
with(response).assertNotNull("$.msg.oauth_token_secret");
}

@Test
public void testUser_idNotNull() {
with(response).assertNotNull("$.msg.user_id");
}

@Test
public void testXmpp_tokenNotNull() {
with(response).assertNotNull("$.msg.xmpp_token");
}
}
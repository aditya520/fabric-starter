// This file is safe to edit. Once it exists it will not be overwritten

package restapi

import (
	"crypto/tls"
	"net/http"

	"github.com/go-openapi/errors"
	"github.com/go-openapi/runtime"
	"github.com/go-openapi/runtime/middleware"
	log "github.com/sirupsen/logrus"

	"fabric_starter/common/utils"
	"fabric_starter/models"
	"fabric_starter/restapi/operations"
	"fabric_starter/restapi/operations/network"

	networkLogic "fabric_starter/logic/network"
)

//go:generate swagger generate server --target ../../fabric_starter --name App --spec ../api/swagger.yml

func configureFlags(api *operations.AppAPI) {
	// api.CommandLineOptionsGroups = []swag.CommandLineOptionsGroup{ ... }
}

func configureAPI(api *operations.AppAPI) http.Handler {
	// configure the api here
	api.ServeError = errors.ServeError

	// Set your custom logger if needed. Default one is log.Printf
	// Expected interface func(string, ...interface{})
	//
	// Example:
	api.Logger = log.Printf

	api.JSONConsumer = runtime.JSONConsumer()

	api.JSONProducer = runtime.JSONProducer()

	api.NetworkCreateHandler = network.CreateHandlerFunc(func(params network.CreateParams) middleware.Responder {
		api.Logger("Endpoint path: " + utils.AsJSON(params.HTTPRequest.RequestURI))
		api.Logger("Endpoint params: " + utils.AsJSON(params))

		msg, err := networkLogic.CreateNetwork(params.Body)
		if err != nil {
			errorMsg := err.Error()
			return network.NewCreateDefault(400).WithPayload(&models.Error{
				Code:    400,
				Message: &errorMsg,
			})
		}

		return network.NewCreateOK().WithPayload(msg)

	})

	api.PreServerShutdown = func() {}

	api.ServerShutdown = func() {}

	return setupGlobalMiddleware(api.Serve(setupMiddlewares))
}

// The TLS configuration before HTTPS server starts.
func configureTLS(tlsConfig *tls.Config) {
	// Make all necessary changes to the TLS configuration here.
}

// As soon as server is initialized but not run yet, this function will be called.
// If you need to modify a config, store server instance to stop it individually later, this is the place.
// This function can be called multiple times, depending on the number of serving schemes.
// scheme value will be set accordingly: "http", "https" or "unix"
func configureServer(s *http.Server, scheme, addr string) {
}

// The middleware configuration is for the handler executors. These do not apply to the swagger.json document.
// The middleware executes after routing but before authentication, binding and validation
func setupMiddlewares(handler http.Handler) http.Handler {
	return handler
}

// The middleware configuration happens before anything, this middleware also applies to serving the swagger.json document.
// So this is a good place to plug in a panic handling middleware, logging and metrics
func setupGlobalMiddleware(handler http.Handler) http.Handler {
	return handler
}

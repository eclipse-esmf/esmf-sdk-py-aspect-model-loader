"""Aspect Model Resolver test suit."""

from unittest import mock

from esmf_aspect_meta_model_python.resolver.base import AspectModelResolver


class TestAspectModelResolver:
    """Aspect Model Resolver test suit."""

    def test__init__(self):
        result = AspectModelResolver("meta_model_resolver", "namespace_resolver")

        assert result._meta_model_resolver == "meta_model_resolver"
        assert result._namespace_resolver == "namespace_resolver"

    @mock.patch("esmf_aspect_meta_model_python.resolver.base.AspectNamespaceResolver")
    @mock.patch("esmf_aspect_meta_model_python.resolver.base.AspectMetaModelResolver")
    def test_init_with_defaults(self, aspect_meta_model_resolver_mock, aspect_namespace_resolver_mock):
        aspect_meta_model_resolver_mock.return_value = "meta_model_resolver"
        aspect_namespace_resolver_mock.return_value = "namespace_resolver"
        result = AspectModelResolver()

        assert result._meta_model_resolver == "meta_model_resolver"
        assert result._namespace_resolver == "namespace_resolver"

    @mock.patch("esmf_aspect_meta_model_python.resolver.base.AspectModelResolver.resolve_namespaces")
    @mock.patch("esmf_aspect_meta_model_python.resolver.base.AspectModelResolver.resolve_meta_model")
    def test_resolve(self, resolve_meta_model_mock, resolve_namespaces_mock):
        aspect_resolver = AspectModelResolver("meta_model_resolver", "namespace_resolver")
        result = aspect_resolver.resolve("graph", "file_path", "samm_version")

        assert result is None
        resolve_meta_model_mock.assert_called_once_with("graph", "samm_version")
        resolve_namespaces_mock.assert_called_once_with("graph", "file_path")

    @mock.patch("esmf_aspect_meta_model_python.resolver.base.AspectMetaModelResolver")
    def test_resolve_meta_model(self, aspect_meta_model_resolver_mock):
        meta_model_resolver_mock = mock.MagicMock(name="meta_model_resolver")
        aspect_meta_model_resolver_mock.return_value = meta_model_resolver_mock
        aspect_resolver = AspectModelResolver(namespace_resolver="namespace_resolver")
        result = aspect_resolver.resolve_meta_model("graph", "samm_version")

        assert result is None
        meta_model_resolver_mock.parse.assert_called_once_with("graph", "samm_version")

    @mock.patch("esmf_aspect_meta_model_python.resolver.base.AspectNamespaceResolver")
    def test_resolve_namespaces(self, aspect_namespace_resolver_mock):
        namespace_resolver_mock = mock.MagicMock(name="namespace_resolver")
        aspect_namespace_resolver_mock.return_value = namespace_resolver_mock
        aspect_resolver = AspectModelResolver(meta_model_resolver="meta_model_resolver")
        result = aspect_resolver.resolve_namespaces("graph", "aspect_file_path")

        assert result is None
        namespace_resolver_mock.parse.assert_called_once_with("graph", "aspect_file_path")

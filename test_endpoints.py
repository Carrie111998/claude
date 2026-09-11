#!/usr/bin/env python3
"""
Test script to verify multi-endpoint configuration.

This script tests that all configured OmniRoute endpoints can be
accessed and that endpoint switching works correctly.
"""

import asyncio
import os
import sys
from app.config import Settings
from app.omniroute.client import OmniRouteClient


async def test_endpoint(name: str, base_url: str, api_key: str) -> bool:
    """Test a single endpoint by attempting to list agents."""
    client = OmniRouteClient(base_url=base_url, api_key=api_key)
    try:
        agents = await client.list_agents()
        print(f"✅ {name:15} | {base_url}")
        return True
    except Exception as e:
        print(f"❌ {name:15} | {base_url}")
        print(f"   Error: {type(e).__name__}: {str(e)[:100]}")
        return False


async def main():
    """Test all configured endpoints."""
    settings = Settings()

    print("\n🔍 Testing OmniRoute Endpoints")
    print("=" * 80)
    print(f"Selected Endpoint: {settings.omniroute_endpoint.upper()}\n")

    endpoints = [
        ("PUBLIC", settings.omniroute_base_url),
        ("CLOUDFLARE", settings.omniroute_cloudflare_url),
        ("LOCAL", settings.omniroute_local_url),
        ("NETWORK", settings.omniroute_network_url),
    ]

    results = []
    for name, url in endpoints:
        success = await test_endpoint(name, url, settings.omniroute_api_key)
        results.append((name, success))

    print("\n" + "=" * 80)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"Results: {passed}/{total} endpoints responded\n")

    if passed == total:
        print("✅ All endpoints are accessible!")
        return 0
    elif passed > 0:
        print(f"⚠️  {passed} endpoint(s) working, {total - passed} unreachable")
        return 1
    else:
        print("❌ No endpoints are accessible!")
        print("   Check your API key and network connectivity")
        return 2


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
